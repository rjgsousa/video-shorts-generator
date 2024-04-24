import json
import unittest
import numpy as np

from deepdiff import DeepDiff

from vsg_themes.analysis.theme_keywords import ThemeKeywords


class TestTfIdf(unittest.TestCase):
    def setUp(self):
        self.tf = ThemeKeywords(threshold=0.15)

    def test_success_given_mocked_data(self):
        data = 'Simple "document" to test the functionality.'

        tfidf_expected_result = \
            {
                0: {'theme': 'functionality', 'score': np.float64(0.5)},
                1: {'theme': 'test', 'score': np.float64(0.5)},
                2: {'theme': 'document', 'score': np.float64(0.5)},
                3: {'theme': 'simple', 'score': np.float64(0.5)}
            }

        tfidf_result = self.tf.conduct_analysis_and_create_report(data, out_file_path=None)

        # assert same dict
        difference = DeepDiff(tfidf_expected_result, tfidf_result)

        assert difference == {}

