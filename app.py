#!/usr/bin/env python
import os
import signal
import subprocess
import logging
from datetime import datetime, timedelta

import requests
import yaml
from retrying import retry


logger = logging.getLogger("app")


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
        logger.warn(f"Error sending metrics to hosted graphite - Status code {response.status_code}")
    else:
        logger.info(f"Metrics sent to hosted graphite - Status code {response.status_code}")


def initialize_metrics():
    initialized_metrics = []
    timestamp = int(get_timestamp())
    with open('config.yaml') as fp:
        config = yaml.load(fp)
        for metric in config['Metrics']:
            stats = metric['Statistics'] if isinstance(metric['Statistics'], list) else [metric['Statistics']]
            for stat in stats:
                metric_name = (metric['Options']['Formatter']
                               .replace("%(statistic)s", stat.lower()))
                initialized_metrics.append("{} 0.0 {}".format(metric_name, timestamp))
    send_to_hostedgraphite("\n".join(initialized_metrics))


@retry(wait_fixed=60000, retry_on_result=lambda res: res is None)
def call_leadbutt():
    """
    See https://github.com/crccheck/cloudwatch-to-graphite for more info on leadbutt
    """
    result = subprocess.Popen("leadbutt", stdout=subprocess.PIPE)
    metrics = result.communicate()[0].decode("utf-8")
    send_to_hostedgraphite(metrics)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
    )

    # python by default installs a signal handler that largely ignores SIGPIPE, but we want to use it for our watchdog
    # mechanism, so reinstate the *unix* default, which is a fatal handler
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    initialize_metrics()
    call_leadbutt()
