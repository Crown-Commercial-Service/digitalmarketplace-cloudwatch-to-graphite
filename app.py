#!/usr/bin/env python
import os
import subprocess
from datetime import datetime, timedelta

import requests
import yaml
from retrying import retry


def get_timestamp():
    return (
        (datetime.now() - timedelta(days=5)) - datetime(1970, 1, 1)
    ).total_seconds()


def send_to_hostedgraphite(metrics):
    response = requests.put(
        "http://www.hostedgraphite.com/api/v1/sink",
        auth=(os.getenv("HOSTED_GRAPHITE_API_KEY"), ""),
        data=metrics
    )

    if response.status_code >= 400:
        print(response.status_code, ": Error sending metrics to hosted graphite")


def initialize_metrics():
    initialized_metrics = []
    timestamp = int(get_timestamp())
    with open('config.yaml') as fp:
        config = yaml.load(fp)
        for metric in config['Metrics']:
            metric_name = (metric['Options']['Formatter']
                           .replace("%(statistic)s", metric['Statistics'].lower()))
            initialized_metrics.append("{} 0.0 {}".format(metric_name, timestamp))
    send_to_hostedgraphite("\n".join(initialized_metrics))


def group_by_metric_name(metrics_list):
    metrics_dict = {}
    keys = set([x.split()[0] for x in metrics_list])
    for key in keys:
        items = list(filter(lambda x: x.split()[0] == key, metrics_list))
        metrics_dict[key] = items

    return metrics_dict


def drop_latest_timestamp(metrics):
    metrics_list = metrics.splitlines()[:-1]
    metrics_dict = group_by_metric_name(metrics_list)
    final_string = ''
    for key, metrics in metrics_dict.items():
        metrics_sorted = sorted(metrics, key=lambda x: int(x.split()[-1]))
        metrics_sorted.pop(-1)
        final_string += "\n".join(metrics_sorted) + "\n"
    return final_string


@retry(wait_fixed=60000, retry_on_result=lambda res: res is None)
def call_leadbutt():
    result = subprocess.Popen("leadbutt", stdout=subprocess.PIPE)
    metrics = result.communicate()[0].decode("utf-8")
    metrics = drop_latest_timestamp(metrics)
    send_to_hostedgraphite(metrics)


if __name__ == '__main__':
    initialize_metrics()
    call_leadbutt()
