import unittest
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from src.pipelines.evaluate import evaluate


class EvaluationCaseTest(unittest.TestCase):
    def test_contains_all_metrics(self):
        y_test = [1, 23, 44, 21]
        predictions = [1, 23, 44, 21]

        report = evaluate(y_test=y_test, predictions=predictions)

        self.assertIsNotNone(report)
        self.assertIsNotNone(report['mse'])
        self.assertIsNotNone(report['r2'])
    
    def test__all_metrics_is_correct(self):
        y_test = [1, 23, 44, 21]
        predictions = [1, 23, 44, 21]

        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        report = evaluate(y_test=y_test, predictions=predictions)

        self.assertIsNotNone(report)
        self.assertEqual(report['mse'], mse)
        self.assertEqual(report['r2'], r2)