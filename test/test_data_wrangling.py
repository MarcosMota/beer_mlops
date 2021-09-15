import contextlib
import functools
import os
import unittest
from unittest.mock import patch, MagicMock
import random
from pyathena.pandas.cursor import PandasCursor
import string
from src.pipelines.wrangling import colect_sample
from sqlalchemy.dialects import registry
from util import with_cursor


registry.register("awsathena.rest", "pyathena.sqlalchemy_athena", "AthenaDialect")

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
S3_PREFIX = "test_pyathena"
WORK_GROUP = "test-pyathena"
SCHEMA = "test_pyathena_" + "".join(
    [random.choice(string.ascii_lowercase + string.digits) for _ in range(10)]
)


class WithConnect(object):
    def connect(self, **opts):
        from pyathena import connect

        return connect(schema_name=SCHEMA, **opts)


class DataWranglingCase(unittest.TestCase, WithConnect):
    @with_cursor(cursor_class=PandasCursor)
    def test_fetchone(self, cursor):
        cursor.execute("SELECT * FROM one_row")
        self.assertEqual(cursor.rownumber, 0)
        self.assertEqual(cursor.fetchone(), (1,))
        self.assertEqual(cursor.rownumber, 1)
        self.assertIsNone(cursor.fetchone())


if __name__ == '__main__':
    unittest.main()
