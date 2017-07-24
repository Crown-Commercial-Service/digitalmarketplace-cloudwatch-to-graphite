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


@retry(wait_fixed=60000, retry_on_result=lambda res: res is None)
def call_leadbutt():
    result = subprocess.Popen("leadbutt", stdout=subprocess.PIPE)
    metrics = result.communicate()[0].decode("utf-8")
    send_to_hostedgraphite(metrics)


if __name__ == '__main__':
    initialize_metrics()
    call_leadbutt()
