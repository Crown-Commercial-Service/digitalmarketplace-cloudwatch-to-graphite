import boto3
import mock
import pytest
import requests
import yaml

from botocore.stub import Stubber
from datetime import datetime
from dateutil.tz import tzutc
from freezegun import freeze_time
from io import StringIO

from app import (
    create_hostedgraphite_base_metrics,
    format_cloudwatch_metric_datapoint_for_hostedgraphite,
    format_config_metric_entry_for_hostedgraphite_base_metric,
    get_config,
    get_metric_from_cloudwatch,
    send_to_hostedgraphite
)

from .fixtures import config


class TestApp:

    def setup_method(self):
        # Mock out boto3 cloudwatch client
        self.client = boto3.client('cloudwatch', region_name="eu-west-1")
        self.stubber = Stubber(self.client)
        self.stubber.activate()

        # Mock out send_to_hostedgraphite method
        self.send_to_hostedgraphite_mock = mock.patch('app.send_to_hostedgraphite')
        self.send_to_hostedgraphite_mock.start()

    def teardown_method(self):
        self.send_to_hostedgraphite_mock.stop()
        self.stubber.deactivate()


class TestGetConfig(TestApp):

    def test_get_config_with_valid_yaml(self):
        fake_config = StringIO("""Metrics:
        - Namespace: "DM-RequestTimeBuckets"
          MetricName: "preview-antivirus-api-request-times-0"
          Statistics: "Sum"
          Dimensions: {}
          Options:
            Formatter: 'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.%(statistic)s'
        - Namespace: "DM-RequestTimeBuckets"
          MetricName: "preview-antivirus-api-request-times-1"
          Statistics: "Sum"
          Dimensions: {}
          Options:
            Formatter: 'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_1.%(statistic)s'
        """)

        with mock.patch('app.open', return_value=fake_config):
            config_dict = get_config()

        assert config_dict == {
            'Metrics':
                [
                    {
                        'Namespace': 'DM-RequestTimeBuckets',
                        'MetricName': 'preview-antivirus-api-request-times-0',
                        'Statistics': 'Sum',
                        'Dimensions': {},
                        'Options': {
                            'Formatter': 'cloudwatch.request_time_buckets.preview.antivirus-api.'
                                         'request_time_bucket_0.%(statistic)s'
                        }
                    },
                    {
                        'Namespace': 'DM-RequestTimeBuckets',
                        'MetricName': 'preview-antivirus-api-request-times-1',
                        'Statistics': 'Sum',
                        'Dimensions': {},
                        'Options': {
                            'Formatter': 'cloudwatch.request_time_buckets.preview.antivirus-api.'
                                         'request_time_bucket_1.%(statistic)s'
                        }
                    }
                ]
        }

    def test_get_config_with_invalid_yaml(self):
        fake_config = StringIO("""}I am not valid yaml!""")
        with mock.patch('app.open', return_value=fake_config), pytest.raises(yaml.YAMLError):

            get_config()


class TestSendToHostedGraphite(TestApp):

    @mock.patch('app.os.getenv', return_value='our_env_value')
    @mock.patch('app.requests.put', return_value=mock.Mock(status_code=200))
    def test_send_to_hostedgraphite(self, put, getenv):
        send_to_hostedgraphite('Some data')

        assert getenv.called_once_with('HOSTED_GRAPHITE_API_KEY')
        assert put.called_once_with(
            "http://www.hostedgraphite.com/api/v1/sink",
            auth=('our_env_value', ''),
            data='Some data'
        )

    @mock.patch('app.logger')
    @mock.patch('app.os.getenv')
    @mock.patch('app.requests.put', return_value=mock.Mock(status_code=200))
    def test_send_to_hostedgraphite_success_logging(self, put, getenv, logger):
        send_to_hostedgraphite('Some data')

        assert logger.info.called_once_with("Metrics sent to hosted graphite - Status code 200")

    @mock.patch('app.logger')
    @mock.patch('app.os.getenv')
    @mock.patch('app.requests.put', return_value=mock.Mock(spec=requests.Response, status_code=404, reason='Not Found'))
    def test_send_to_hostedgraphite_failure_logging(self, put, getenv, logger):
        send_to_hostedgraphite('Some data')

        assert logger.warning.called_once_with("Error sending metrics to hosted graphite - 404: Not Found")

    @mock.patch('app.os.getenv')
    @mock.patch('app.requests.put', side_effect=requests.ConnectionError('Timeout'))
    def test_send_to_hostedgraphite_failure(self, put, getenv):
        with pytest.raises(requests.ConnectionError):
            send_to_hostedgraphite('Some data')


class TestFormatCloudwatchMetricDatapointForHostedgraphite(TestApp):

    def test_format_cloudwatch_metric_datapoint_for_hostedgraphite(self):
        config_entry = {
            'Namespace': 'DM-RequestTimeBuckets',
            'MetricName': 'preview-antivirus-api-request-times-0',
            'Statistics': 'Sum',
            'Dimensions': {},
            'Options': {
                'Formatter': 'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.%(statistic)s'
            }
        }
        metric_datapoint = {'Timestamp': datetime(2018, 9, 20, 14, 18, tzinfo=tzutc()), 'Sum': 1.0, 'Unit': 'None'}

        expected_result = (
            'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 1.0 1537453080'
        )

        assert format_cloudwatch_metric_datapoint_for_hostedgraphite(config_entry, metric_datapoint) == expected_result


class TestFormatConfigMetricEntryForHostedgraphiteBaseMetric(TestApp):

    def test_format_config_metric_entry_for_hostedgraphite_base_metric(self):
        config_entry = {
            'Namespace': 'DM-RequestTimeBuckets',
            'MetricName': 'preview-antivirus-api-request-times-0',
            'Statistics': 'Sum',
            'Dimensions': {},
            'Options': {
                'Formatter': 'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.%(statistic)s'
            }
        }
        timestamp = 1234567890

        assert (
            format_config_metric_entry_for_hostedgraphite_base_metric(config_entry, timestamp) ==
            'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1234567890'
        )


class TestCreateHostedgraphiteBaseMetric(TestApp):

    @freeze_time("2018-09-21 16:00:00")
    def test_create_hostedgraphite_base_metrics(self):
        base_metrics = create_hostedgraphite_base_metrics(config)

        assert base_metrics == [
            'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537113600',
            'cloudwatch.application_500s.preview.api.500s.sum 0.0 1537113600',
            'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 0.0 1537113600'
        ]


class TestGetMetricFromCloudwatch(TestApp):

    @freeze_time("2018-09-21 16:00:00")
    def test_get_metric_from_cloudwatch(self):
        config_metric_entry = {
            'Namespace': 'DM-RequestTimeBuckets',
            'MetricName': 'preview-antivirus-api-request-times-0',
            'Statistics': 'Sum',
            'Dimensions': {},
            'Options': {
                'Formatter': 'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.%(statistic)s'
            }
        }

        self.client.get_metric_statistics = mock.Mock()

        get_metric_from_cloudwatch(self.client, config_metric_entry)

        self.client.get_metric_statistics.assert_called_once_with(
            Period=60,
            StartTime=datetime(2018, 9, 21, 15, 50),
            EndTime=datetime(2018, 9, 21, 16, 0),
            MetricName='preview-antivirus-api-request-times-0',
            Namespace='DM-RequestTimeBuckets',
            Statistics=['Sum'],
            Dimensions=[],
            Unit='None',
        )
