import unittest

import boto3
from moto import mock_s3, mock_kinesis

S3_BUCKET_NAME = 'amaksimov-s3-bucket'
DEFAULT_REGION = 'us-east-1'
from moto.core import ACCOUNT_ID

S3_TEST_FILE_KEY = 'prices/new_prices.json'
S3_TEST_FILE_CONTENT = [
    {"product": "Apple", "price": 15},
    {"product": "Orange", "price": 25}
]
@mock_kinesis()
@mock_s3
class DataIngestionCase(unittest.TestCase):
    def test_getbeers_with_success(self):
        self.assertEqual(True, True)

    def test_getbeers_with_fail(self):
        self.assertEqual(True, False)

    def test_clear_dataset_with_success(self):
        self.assertEqual(True, False)

    def test_clear_dataset_with_fail(self):
        self.assertEqual(True, False)

    @mock_kinesis
    def test_describe_stream_summary(self):
        conn = boto3.client("kinesis", region_name="us-west-2")
        stream_name = "my_stream_summary"
        shard_count = 5
        conn.create_stream(StreamName=stream_name, ShardCount=shard_count)

        resp = conn.describe_stream_summary(StreamName=stream_name)
        stream = resp["StreamDescriptionSummary"]
        print()
        print(stream_name)
        self.assertEqual(stream["StreamName"], stream_name)
        stream["StreamName"].should.equal(stream_name)
        stream["OpenShardCount"].should.equal(shard_count)
        stream["StreamARN"].should.equal(
            "arn:aws:kinesis:us-west-2:{}:{}".format(ACCOUNT_ID, stream_name)
        )
        stream["StreamStatus"].should.equal("ACTIVE")

if __name__ == '__main__':
    unittest.main()
