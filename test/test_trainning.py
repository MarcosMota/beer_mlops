from numpy import histogram
from numpy.core.fromnumeric import mean
import pandas as pd
import numpy as np
import unittest
from unittest.mock import patch, Mock

from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor


from src.pipelines.training import load_data, train_fn, save_model


class TrainningCaseTest(unittest.TestCase):

    def setUp(self):
        self.X_train = np.array([
            [-1.41398638, -1.41420892, -1.20270298,  1.40693001,  1.41418395],
            [ 0.68504121,  0.71024095, -0.04295368, -0.82760589, -0.69916691],
            [ 0.72894517,  0.70396797,  1.24565666, -0.57932412, -0.71501704]
        ])
        self.y_train = np.array([55, 50, 60])
        
    @patch("pandas.read_csv")
    @patch("pandas.read_csv")
    def test_load_dataset_with_success(self, read_csv_mock_features: Mock, read_csv_mock_label: Mock):
        read_csv_mock_features.return_value = pd.DataFrame(self.X_train)
        read_csv_mock_label.return_value = pd.DataFrame(self.y_train)
        X_train, y_train = load_data(training_dir='')

        self.assertIsNotNone(X_train)
        self.assertIsNotNone(y_train)
    
    def test_trainning_with_success(self):
        hyperparameters = {
            'max_depth' : 2,
            'n_estimators' : 1,
            'random_state' : None
        }

        model = train_fn(X_train=self.X_train,y_train=self.y_train, hyperparameters=hyperparameters)

        print(model.get_params())
        self.assertIsNotNone(model)

    @patch("joblib.dump")
    def test_save_model_with_success(self, joblib_dump: Mock):

        model: BaseEstimator = RandomForestRegressor()
        
        save_model('', model)

        joblib_dump.assert_called_once()