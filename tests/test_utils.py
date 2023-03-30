import unittest

import pandas as pd

from src.app import create_app
from src.app.graphs.utils import read_logs


class TestUtils(unittest.TestCase):
    def setUp(self):

        self.app = create_app()

    def test_read_logs(self):

        # setup application context
        with self.app.app_context():

            # without params
            count, df = read_logs()
            self.assertIsInstance(count, int)
            self.assertIsInstance(df, pd.DataFrame)

            # with params
            count, status_codes, mime_types = read_logs(1)
            self.assertIsInstance(count, int)
            self.assertIsInstance(status_codes, list)
            self.assertIsInstance(mime_types, list)
