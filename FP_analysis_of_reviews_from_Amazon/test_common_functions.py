from unittest import TestCase, main
from common_functions import (
    run_func_parallel,
    get_apps_scores,
    get_dict_of_apps_with_score,
    AppScore,
)

class TestRunFuncParallel(TestCase):
    def setUp(self):
        self.data1 = ["a", "b", "c"]
        self.data2 = [0]
    def test_run_func_parallel(self):
        self.assertEqual(run_func_parallel(len, [self.data1, self.data2]), [3, 1])

class TestGetAppsScores(TestCase):
    def test_get_apps_scores(self):
        data = [
            {"asin": "1", "overall": 1.0},
            {"asin": "2", "overall": 5.0},
            {"asin": "1", "overall": 5.0},
            {"asin": "2", "overall": 4.0},
            {"asin": "3", "overall": 4.0},
        ]
        self.assertEqual(
            get_apps_scores(data), {"1": [1.0, 5.0], "2": [5.0, 4.0], "3": [4.0]}
        )
    def test_get_dict_of_apps_with_score_without_one_overall(self):
        data = [
            {"asin": "1"},
            {"asin": "2", "overall": 5.0},
            {"asin": "1", "overall": 5.0},
            {"asin": "2", "overall": 4.0},
            {"asin": "3", "overall": 4.0},
        ]
        self.assertEqual(
            get_apps_scores(data), {"1": [5.0], "2": [5.0, 4.0], "3": [4.0]}
        )
    def test_get_apps_scores_without_overall(self):
        data = [
            {"asin": "1"},
            {"asin": "2"},
            {"asin": "1"},
            {"asin": "2"},
            {"asin": "3"},
        ]
        self.assertEqual(get_apps_scores(data), {"1": [], "2": [], "3": []})

class TestGetDictOfAppsWithScore(TestCase):
    def test_get_dict_of_apps_with_score(self):
        data1 = [
            {"asin": "1", "overall": 1.0},
            {"asin": "2", "overall": 5.0},
            {"asin": "1", "overall": 5.0},
        ]
        data2 = [{"asin": "2", "overall": 4.0}, {"asin": "3", "overall": 4.0}]
        self.assertEqual(
            get_dict_of_apps_with_score([data1, data2]),
            {
                "1": AppScore(asin="1", total_score=6.0, number_of_votes=2),
                "2": AppScore(asin="2", total_score=9.0, number_of_votes=2),
                "3": AppScore(asin="3", total_score=4.0, number_of_votes=1),
            },
        )
    def test_get_dict_of_apps_with_score_without_one_overall(self):
        data1 = [
            {"asin": "1"},
            {"asin": "2", "overall": 5.0},
            {"asin": "1", "overall": 5.0},
        ]
        data2 = [{"asin": "2", "overall": 4.0}, {"asin": "3", "overall": 4.0}]
        self.assertEqual(
            get_dict_of_apps_with_score([data1, data2]),
            {
                "1": AppScore(asin="1", total_score=5.0, number_of_votes=1),
                "2": AppScore(asin="2", total_score=9.0, number_of_votes=2),
                "3": AppScore(asin="3", total_score=4.0, number_of_votes=1),
            },
        )
    def test_get_dict_of_apps_with_score_without_overall(self):
        data1 = [
            {"asin": "1"},
            {"asin": "2"},
            {"asin": "1"},
        ]
        data2 = [{"asin": "2"}, {"asin": "3"}]
        self.assertEqual(
            get_dict_of_apps_with_score([data1, data2]),
            {
                "1": AppScore(asin="1", total_score=0.0, number_of_votes=0),
                "2": AppScore(asin="2", total_score=0.0, number_of_votes=0),
                "3": AppScore(asin="3", total_score=0.0, number_of_votes=0),
            },
        )


if __name__ == "__main__":
    main(verbosity=2)
