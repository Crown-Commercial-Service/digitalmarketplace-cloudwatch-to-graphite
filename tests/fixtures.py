"""File containing test fixtures for tests."""
from datetime import datetime
from dateutil.tz import tzutc
from io import StringIO


config_yaml = StringIO("""Metrics:
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


config = {'Metrics': [
    {
        'Namespace': 'DM-RequestTimeBuckets',
        'MetricName': 'preview-antivirus-api-request-times-0',
        'Statistics': 'Sum',
        'Dimensions': {},
        'Options': {
            'Formatter': 'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.%(statistic)s'
        }
    },
    {
        'Namespace': 'DM-500s',
        'MetricName': 'preview-api-nginx-500s',
        'Statistics': 'Sum',
        'Dimensions': {},
        'Options': {'Formatter': 'cloudwatch.application_500s.preview.api.500s.%(statistic)s'}
    },
    {
        'Namespace': 'AWS/Logs',
        'MetricName': 'IncomingLogEvents',
        'Statistics': 'Sum',
        'Dimensions': {'LogGroupName': 'preview-search-api-nginx'},
        'Options': {'Formatter': 'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.%(statistic)s'}
    }
]}


responses = (
    {
        'Label': 'preview-antivirus-api-request-times-0',
        'Datapoints': [
            {'Timestamp': datetime(2018, 9, 20, 14, 18, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 13, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 19, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 14, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 20, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 15, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 17, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 21, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 12, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 16, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'}
        ],
        'ResponseMetadata': {
            'RequestId': 'b06efdb7-bce0-11e8-96de-d9e39d5d8a92',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'x-amzn-requestid': 'b06efdb7-bce0-11e8-96de-d9e39d5d8a92',
                'content-type': 'text/xml',
                'content-length': '1697',
                'date': 'Thu, 20 Sep 2018 14:23:04 GMT'
            },
            'RetryAttempts': 0
        }
    },
    {
        'Label': 'preview-api-nginx-500s',
        'Datapoints': [
            {'Timestamp': datetime(2018, 9, 20, 14, 18, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 13, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 19, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 14, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 20, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 15, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 17, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 21, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 12, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 16, tzinfo=tzutc()), 'Sum': 0.0, 'Unit': 'None'}
        ],
        'ResponseMetadata': {
            'RequestId': 'b073dfbf-bce0-11e8-96de-d9e39d5d8a92',
            'HTTPStatusCode': 200,
            'HTTPHeaders':
                {
                    'x-amzn-requestid': 'b073dfbf-bce0-11e8-96de-d9e39d5d8a92',
                    'content-type': 'text/xml',
                    'content-length': '1682',
                    'date': 'Thu, 20 Sep 2018 14:23:04 GMT'
                },
            'RetryAttempts': 0
        }
    },
    {
        'Label': 'IncomingLogEvents',
        'Datapoints': [
            {'Timestamp': datetime(2018, 9, 20, 14, 18, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 13, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 19, tzinfo=tzutc()), 'Sum': 147.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 14, tzinfo=tzutc()), 'Sum': 147.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 20, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 15, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 17, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 21, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 12, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'},
            {'Timestamp': datetime(2018, 9, 20, 14, 16, tzinfo=tzutc()), 'Sum': 2.0, 'Unit': 'None'}
        ],
        'ResponseMetadata': {
            'RequestId': 'b077d667-bce0-11e8-96de-d9e39d5d8a92',
            'HTTPStatusCode': 200,
            'HTTPHeaders':
                {
                    'x-amzn-requestid': 'b077d667-bce0-11e8-96de-d9e39d5d8a92',
                    'content-type': 'text/xml',
                    'content-length': '1681',
                    'date': 'Thu, 20 Sep 2018 14:23:04 GMT'
                },
            'RetryAttempts': 0
        }
    }
)


results = (
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537453080',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537452780',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537453140',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537452840',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537453200',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537452900',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537453020',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537453260',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537452720',
    'cloudwatch.request_time_buckets.preview.antivirus-api.request_time_bucket_0.sum 0.0 1537452960',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537453080',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537452780',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537453140',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537452840',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537453200',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537452900',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537453020',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537453260',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537452720',
    'cloudwatch.application_500s.staging.api.500s.sum 0.0 1537452960',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537453080',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537452780',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 147.0 1537453140',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 147.0 1537452840',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537453200',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537452900',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537453020',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537453260',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537452720',
    'cloudwatch.incoming_log_events.preview.search-api.nginx_logs.sum 2.0 1537452960'
)
