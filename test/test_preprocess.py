from numpy.core.fromnumeric import mean
import pandas as pd

import unittest
from unittest.mock import patch, Mock

from src.pipelines.preprocessing import clear_fn, load_dataset, preprocess_fn


class PreprocessCaseTest(unittest.TestCase):

    def setUp(self):
        self.columns = ["id","name","ibu","target_fg","target_og","ebc","srm","ph"]
        self.rows =   [                    
                    [293,'I Wanna Be Your Dog', 55.0,1035.0,1125.0,600.0,305.0,4.1],
                    [51, 'TM10', 20.0, 1005.0, 1048.0, 14.0, 7.0, 4.2],
                    [188, 'Paradox Jura', 55.0, 1014.0, 1128.0, 300.0, 152.0, 4.4],
                    [188, 'Paradox', 55.70, 10.0, 112.0, 30.0, 1529.0, 44.4],
                ]
        self.test_df =  pd.DataFrame(
                self.rows,
                columns=self.columns,
            )
        
    @patch("pandas.read_csv")
    def test_load_dataset_with_success(self, read_csv_mock: Mock):
        read_csv_mock.return_value = self.test_df
        df = load_dataset(input_data_path='')

        columns = list(df.columns.values)

        self.assertIsNotNone(df)
        self.assertListEqual(columns, self.columns)
    
    def test_clear_dataset_with_success(self):
        columns_cleaned = ["target_fg","target_og","ebc","srm","ph","ibu"]
        df = clear_fn(self.test_df)

        columns = list(df.columns.values)

        self.assertIsNotNone(df)
        self.assertListEqual(columns, columns_cleaned)
        self.assertEqual(df.duplicated().sum(), 0)

    def test_preprocess_dataset_with_success(self):
        split_ratio = .25
        dataset_size = len(self.test_df)
        test_size = int(dataset_size * split_ratio)

        X_train, X_test, y_train, y_test = preprocess_fn(clear_fn(self.test_df), split_ratio=split_ratio)

        self.assertIsNotNone(X_train)
        self.assertIsNotNone(X_test)
        self.assertIsNotNone(y_train)
        self.assertIsNotNone(y_test)

        self.assertEqual(len(X_test), test_size)
