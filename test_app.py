from app import drop_latest_timestamp

TEST_DATA = """cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 143.0 1499944620
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 146.0 1499944320
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 139.0 1499944140
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 99.0 1499944680
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 109.0 1499944380
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 92.0 1499944200
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 109.0 1499944440
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 224.0 1499944560
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 215.0 1499944260
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 96.0 1499944500
my.random.metric.name.string 996.0 1000
my.random.metric.name.string 396.0 2000
my.random.metric.name.string 446.0 3000
my.random.metric.name.string 96.0 4000
my.random.metric.name.string 95.0 5000
my.random.metric.name.string 986.0 6000
my.random.metric.name.string 956.0 7000
my.random.metric.name.string 296.0 8000
my.random.metric.name.string 196.0 9000
my.random.metric.name.string 906.0 10000
"""

EXPECTED = """my.random.metric.name.string 996.0 1000
my.random.metric.name.string 396.0 2000
my.random.metric.name.string 446.0 3000
my.random.metric.name.string 96.0 4000
my.random.metric.name.string 95.0 5000
my.random.metric.name.string 986.0 6000
my.random.metric.name.string 956.0 7000
my.random.metric.name.string 296.0 8000
my.random.metric.name.string 196.0 9000
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 139.0 1499944140
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 92.0 1499944200
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 215.0 1499944260
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 146.0 1499944320
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 109.0 1499944380
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 109.0 1499944440
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 96.0 1499944500
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 224.0 1499944560
cloudwatch.request_time_buckets.production.api.request_time_bucket_0.samplecount 143.0 1499944620
"""


def test_drop_latest_timestamp():
    assert EXPECTED == drop_latest_timestamp(TEST_DATA)
