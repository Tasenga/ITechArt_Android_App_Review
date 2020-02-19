from unittest import TestCase, main
from common_functions import (
    run_func_parallel,
    get_apps_scores,
    get_dict_of_apps_with_score,
)

class TestRunFuncParallel(TestCase):
    def setUp(self):
        self.data1 = ["a", "b", "c"]
        self.data2 = [0]
    def test_run_func_parallel(self):
        self.assertEqual(run_func_parallel(len, [self.data1, self.data2]), [3, 1])

class TestGetAppsScores(TestCase):
    def setUp(self):
        self.data = [
            {"asin": "1", "overall": 1.0},
            {"asin": "2", "overall": 5.0},
            {"asin": "1", "overall": 5.0},
            {"asin": "2", "overall": 4.0},
            {"asin": "3", "overall": 4.0},
        ]
    def test_get_apps_scores(self):
        self.assertEqual(
            get_apps_scores(self.data), {"1": [1.0, 5.0], "2": [5.0, 4.0], "3": [4.0]}
        )
    def test_get_apps_scores_with_overall_exc(self):
        self.data[0].pop("overall")
        self.assertEqual(
            get_apps_scores(self.data), {"1": [5.0], "2": [5.0, 4.0], "3": [4.0]}
        )
    def test_get_apps_scores_without_overall(self):
        self.data[0].pop("overall")
        self.data[1].pop("overall")
        self.data[2].pop("overall")
        self.data[3].pop("overall")
        self.data[4].pop("overall")
        self.assertEqual(get_apps_scores(self.data), {"1": [], "2": [], "3": []})

class TestGetDictOfAppsWithScore(TestCase):
    def setUp(self):
        self.data1 = [
            {"asin": "1", "overall": 1.0},
            {"asin": "2", "overall": 5.0},
            {"asin": "1", "overall": 5.0},
        ]
        self.data2 = [{"asin": "2", "overall": 4.0}, {"asin": "3", "overall": 4.0}]
    def test_get_dict_of_apps_with_score(self):
        result = get_dict_of_apps_with_score([self.data1, self.data2])
        self.assertCountEqual(result.keys(), ["1", "2", "3"])
        self.assertEqual(result["1"].asin, "1")
        self.assertEqual(result["1"].total_score, 6)
        self.assertEqual(result["1"].number_of_votes, 2)
        self.assertEqual(result["3"].asin, "3")
        self.assertEqual(result["3"].total_score, 4)
        self.assertEqual(result["3"].number_of_votes, 1)
    def test_get_dict_of_apps_with_score_with_overall_exc(self):
        self.data1[0].pop("overall")
        result = get_dict_of_apps_with_score([self.data1, self.data2])
        self.assertCountEqual(result.keys(), ["1", "2", "3"])
        self.assertEqual(result["1"].asin, "1")
        self.assertEqual(result["1"].total_score, 5)
        self.assertEqual(result["1"].number_of_votes, 1)
        self.assertEqual(result["3"].asin, "3")
        self.assertEqual(result["3"].total_score, 4)
        self.assertEqual(result["3"].number_of_votes, 1)
    def test_get_dict_of_apps_with_score_without_overall(self):
        self.data1[0].pop("overall")
        self.data1[1].pop("overall")
        self.data1[2].pop("overall")
        self.data2[0].pop("overall")
        self.data2[1].pop("overall")
        result = get_dict_of_apps_with_score([self.data1, self.data2])
        self.assertCountEqual(result.keys(), ["1", "2", "3"])
        self.assertEqual(result["1"].asin, "1")
        self.assertEqual(result["1"].total_score, 0)
        self.assertEqual(result["1"].number_of_votes, 0)
        self.assertEqual(result["3"].asin, "3")
        self.assertEqual(result["3"].total_score, 0)
        self.assertEqual(result["3"].number_of_votes, 0)

if __name__ == "__main__":
    main(verbosity=2)
