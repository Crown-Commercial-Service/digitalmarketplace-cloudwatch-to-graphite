#!/usr/bin/env python
import logging
import os
import sys

from datetime import datetime, timedelta
import boto3
import requests
import yaml
from retrying import retry


logger = logging.getLogger("app")


def get_config():
    """Get the config file."""
    with open('config.yaml') as fp:
        config = yaml.load(fp)
    return config


def send_to_hostedgraphite(metrics):
    """Put request to hostedgraphite."""
    response = requests.put(
        "http://www.hostedgraphite.com/api/v1/sink",
        auth=(os.getenv("HOSTED_GRAPHITE_API_KEY"), ""),
        data=metrics
    )

    if not response.ok:
        logger.warning(
            "Error sending metrics to hosted graphite - {}: {}".format(response.status_code, response.reason)
        )
    else:
        logger.info("Metrics sent to hosted graphite - Status code {}".format(response.status_code))


def format_config_metric_entry_for_hostedgraphite_base_metric(config_metric_entry, timestamp):
    hostedgraphite_metric_name = config_metric_entry['Options']['Formatter'].replace(
        "%(statistic)s",
        config_metric_entry['Statistics'].lower()
    )
    hostedgraphite_base_metric = "{} 0.0 {}".format(hostedgraphite_metric_name, timestamp)
    return hostedgraphite_base_metric


def create_hostedgraphite_base_metrics(config):
    """Take a metric entry from the config format it into a base metric used to initialise the metric on hostedgraphite.
    """
    base_metrics = []
    timestamp = int(((datetime.now() - timedelta(days=5)) - datetime(1970, 1, 1)).total_seconds())
    for config_metric_entry in config['Metrics']:
        hostedgraphite_base_metric = format_config_metric_entry_for_hostedgraphite_base_metric(
            config_metric_entry,
            timestamp
        )
        hostedgraphite_base_metrics.append(hostedgraphite_base_metric)
    return hostedgraphite_base_metrics


def format_cloudwatch_metric_datapoint_for_hostedgraphite(metric, result):
    """Given a cloudwatch metric datapoint convert it into the format hostedgraphite expects."""
    hostedgraphite_metric_name = (
        cloudwatch_metric_datapoint['Options']['Formatter'] % {'statistic': cloudwatch_metric_datapoint['Statistics']}
    ).lower()
    return '{0} {1} {2}'.format(
        hostedgraphite_metric_name,
        result[cloudwatch_metric_datapoint['Statistics']],
        result['Timestamp'].strftime('%s')
    )


def get_metric_from_cloudwatch(client, metric):
    """Call the client once for th supplied metric."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(seconds=600)
    return client.get_metric_statistics(
        Period=60,
        StartTime=start_time,
        EndTime=end_time,
        MetricName=metric['MetricName'],
        Namespace=metric['Namespace'],
        Statistics=[metric['Statistics']],
        Dimensions=[{'Name': k, 'Value': v} for k, v in metric['Dimensions'].items()],
        Unit=metric.get('Unit', 'None'),
    )


def get_metrics_from_cloudwatch_and_format_for_hostedgraphite(config):
    """Get metrics from config, call cloudwatch for metric entry and format metric datapoints to expected hostedgraphite
    format.

    For each metric in the config call the cloudwatch api to return the datapoints for that metric.
    For each cloudwatch datapoint create one hostedgraphite metric entry for supply to hostedgraphite.
    """
    hostedgraphite_metrics = []

    client = boto3.client('cloudwatch', region_name="eu-west-1")
    for metric_entry in config['Metrics']:
        cloudwatch_metric = get_metric_from_cloudwatch(client, metric_entry)
        for cloudwatch_metric_datapoint in cloudwatch_metric['Datapoints']:
            hostedgraphite_metric = format_cloudwatch_metric_datapoint_for_hostedgraphite(
                metric_entry,
                cloudwatch_metric_datapoint
            )
            hostedgraphite_metrics.append(hostedgraphite_metric)

    return hostedgraphite_metrics


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s", stream=sys.stdout)
    config = get_config()

    base_metrics = create_hostedgraphite_base_metrics(config)
    send_to_hostedgraphite("\n".join(base_metrics))

    @retry(wait_fixed=60000, retry_on_result=lambda res: res is None)
    def sleep_and_send_retry():
        """Wrapper to apply retry to get and send methods."""
        hostedgraphite_metrics = get_metrics_from_cloudwatch_and_format_for_hostedgraphite(config)
        send_to_hostedgraphite('\n'.join(hostedgraphite_metrics))

    sleep_and_send_retry()
