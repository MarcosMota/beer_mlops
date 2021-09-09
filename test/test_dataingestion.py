import os
import unittest
from src.preprocess.extraction import fn_extraction


class DataIngestionCase(unittest.TestCase):

    def test_environment_region_required(self):
        os.environ['PROJECT_STEAM'] = "teste"

        with self.assertRaises(Exception) as context:
            func = fn_extraction.handler('', '')

    def test_environment_steam_required(self):
        os.environ['AWS_REGION'] = 'teste'

        with self.assertRaises(Exception) as context:
            func = fn_extraction.handler('', '')

        # self.assertTrue('Variáveis AWS_REGION e PROJECT_STEAM não estão definidas' in context.exception)


if __name__ == '__main__':
    unittest.main()
