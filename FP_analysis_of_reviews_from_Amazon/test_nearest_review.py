from unittest import TestCase, mock, main
from nearest_review import (
    ReviewTimeInfo,
    prepare_data,
    count_deltatime,
    get_unix_diff_per_name,
    get_potential_bots,
    filter_bot_review,
    process_data,
    analyze_bots_comments,
    get_nearest_reviews,
)

class TestPrepareData(TestCase):
    def setUp(self):
        # min set of keys in dictionaries(might be more)
        self.data = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 200,},
            {"reviewerID": "1", "reviewText": "b", "unixReviewTime": 300},
            {"reviewerID": "1", "reviewText": "d", "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 500},
        ]
    def test_basic_work(self):
        result = prepare_data(self.data)
        self.assertIsInstance(result, dict)
        self.assertTrue(v is ReviewTimeInfo for v in result.values())
        self.assertCountEqual(result.keys(), ["1", "2"])
        self.assertTrue(len(result["1"]) == 3)
        self.assertTrue(len(result["2"]) == 1)
        self.assertEqual(result["1"][0].time, self.data[2]["unixReviewTime"])
        self.assertEqual(result["1"][1].time, self.data[0]["unixReviewTime"])
        self.assertEqual(result["1"][2].time, self.data[1]["unixReviewTime"])
        self.assertEqual(result["1"][0].text, self.data[2]["reviewText"])
        self.assertEqual(result["1"][1].text, self.data[0]["reviewText"])
        self.assertEqual(result["1"][2].text, self.data[1]["reviewText"])
        self.assertTrue(
            i.text is str or i.text is None for v in result.values() for i in v
        )

class TestCountDeltatime(TestCase):
    def setUp(self):
        # for each value in result function 'prepare_data
        self.data1 = [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")]
        self.data2 = [
            ReviewTimeInfo(100, None),
            ReviewTimeInfo(300, "c"),
            ReviewTimeInfo(400, "d"),
        ]
    def test_count_deltatime(self):
        self.assertEqual(count_deltatime(self.data1), [0, "b", "a"])
        self.assertEqual(count_deltatime(self.data2), [100, "d", "c"])
        with self.assertRaises(Exception):
            self.data1[0].time = 200
            count_deltatime(self.data1)
        with self.assertRaises(Exception):
            self.data2[1].time = 500
            count_deltatime(self.data2)

class TestGetUnixDiffPerName(TestCase):
    def setUp(self):
        # result function 'prepare_data
        self.data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")],
            "2": [
                ReviewTimeInfo(100, None),
                ReviewTimeInfo(300, "c"),
                ReviewTimeInfo(400, "d"),
            ],
            "3": [ReviewTimeInfo(200, None)],
        }
    def test_get_unix_diff_per_name(self):
        self.assertEqual(
            get_unix_diff_per_name(self.data),
            [
                ["1", [0, "b", "a"]],
                ["2", [100, "d", "c"]],
                ["3", ["single_review", "single_review", "single_review"]],
            ],
        )

class TestGetPotentialBots(TestCase):
    # result function 'unix_dict_per_name'
    def setUp(self):
        self.data = [
            ["1", [0, "b", "c"]],
            ["2", [100, "d", "c"]],
            ["3", ["single_review", "single_review", "single_review"]],
            ["4", [0, "e", "f"]],
        ]
    def test_get_potential_bots(self):
        self.assertCountEqual(get_potential_bots(self.data), {"1", "4", None})
        self.assertCountEqual(get_potential_bots(), set())
        self.assertCountEqual(get_potential_bots([["1", [100, "b", "c"]]]), {None})

class TestFilterBotReview(TestCase):
    def setUp(self):
        # result function 'prepare_data
        self.data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")],
            "2": [
                ReviewTimeInfo(100, None),
                ReviewTimeInfo(300, "c"),
                ReviewTimeInfo(400, "d"),
            ],
            "3": [ReviewTimeInfo(200, None)],
        }
        self.bots = {"1", None}
    def test_filter_bot_review(self):
        def check_result(data, bots):
            analyzed_data, number_of_bot_comments = filter_bot_review(data, bots)
            self.assertIsInstance(analyzed_data, dict)
            self.assertTrue(v is ReviewTimeInfo for v in analyzed_data.values())
            self.assertTrue(len(analyzed_data["2"]) == 3)
            self.assertTrue(len(analyzed_data["3"]) == 1)
            self.assertEqual(analyzed_data["2"][0].time, 100)
            self.assertEqual(analyzed_data["2"][1].time, 300)
            self.assertEqual(analyzed_data["2"][2].time, 400)
            self.assertEqual(analyzed_data["3"][0].time, 200)
            self.assertEqual(analyzed_data["2"][1].text, "c")
            self.assertEqual(analyzed_data["3"][0].text, None)
            self.assertTrue(
                i.text is str or i.text is None
                for v in analyzed_data.values()
                for i in v
            )
        check_result(self.data, self.bots)
        self.assertCountEqual(
            filter_bot_review(self.data, self.bots)[0].keys(), ["2", "3"]
        )
        self.assertEqual(filter_bot_review(self.data, self.bots)[1], 2)

        # without bots
        check_result(self.data, set())
        self.assertCountEqual(
            filter_bot_review(self.data, set())[0].keys(), ["1", "2", "3"]
        )
        self.assertEqual(filter_bot_review(self.data, set())[1], 0)

        check_result(self.data, {None})
        self.assertCountEqual(
            filter_bot_review(self.data, {None})[0].keys(), ["1", "2", "3"]
        )
        self.assertEqual(filter_bot_review(self.data, {None})[1], 0)

        # if all comments were written by bots
        analyzed_data, number_of_bot_comments = filter_bot_review(
            self.data, {"1", "2", "3"}
        )
        self.assertCountEqual(analyzed_data.keys(), [])
        self.assertEqual(number_of_bot_comments, 6)

class TestProcessData(TestCase):
    def setUp(self):
        self.data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")],
            "2": [
                ReviewTimeInfo(100, None),
                ReviewTimeInfo(300, "c"),
                ReviewTimeInfo(400, "d"),
            ],
            "3": [ReviewTimeInfo(200, None)],
        }
    def test_process_data_with_bots(self):
        analyzed_data, potential_bots, number_of_bot_comments = process_data(self.data)
        self.assertIsInstance(analyzed_data, dict)
        self.assertTrue(v is ReviewTimeInfo for v in analyzed_data.values())
        self.assertCountEqual(analyzed_data.keys(), ["2", "3"])
        self.assertTrue(len(analyzed_data["2"]) == 3)
        self.assertEqual(analyzed_data["2"][0].time, 100)
        self.assertEqual(analyzed_data["2"][0].text, None)
        self.assertEqual(analyzed_data["2"][1].time, 300)
        self.assertEqual(analyzed_data["2"][1].text, "c")
        self.assertEqual(analyzed_data["2"][2].time, 400)
        self.assertEqual(analyzed_data["2"][2].text, "d")
        self.assertEqual(analyzed_data["2"][1].time, 300)
        self.assertEqual(analyzed_data["2"][1].text, "c")
        self.assertEqual(analyzed_data["3"][0].time, 200)
        self.assertEqual(analyzed_data["3"][0].text, None)
        self.assertCountEqual(potential_bots, {"1", None})
        self.assertEqual(number_of_bot_comments, 2)
    def test_process_data_without_bots(self):
        self.data["1"][1].time = 300
        analyzed_data, potential_bots, number_of_bot_comments = process_data(self.data)
        self.assertCountEqual(analyzed_data.keys(), ["1", "2", "3"])
        self.assertCountEqual(potential_bots, {None})
        self.assertEqual(number_of_bot_comments, 0)

class TestAnalyzeBotsComments(TestCase):
    def setUp(self):
        self.data1 = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 200,},
            {"reviewerID": "2", "reviewText": "e", "unixReviewTime": 500},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 400},
        ]
        self.data2 = [
            {"reviewerID": "1", "reviewText": "b", "unixReviewTime": 300},
            {"reviewerID": "1", "reviewText": "d", "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 500},
        ]
    def test_analyze_bots_comments_with_bots(self):
        (
            sorted_data_without_bot_comments,
            all_number_of_bot_comments,
        ) = analyze_bots_comments([self.data1, self.data2])
        self.assertIsInstance(sorted_data_without_bot_comments, dict)
        self.assertTrue(
            v is ReviewTimeInfo for v in sorted_data_without_bot_comments.values()
        )
        self.assertCountEqual(sorted_data_without_bot_comments.keys(), ["1"])
        self.assertTrue(len(sorted_data_without_bot_comments["1"]) == 3)
        self.assertEqual(sorted_data_without_bot_comments["1"][0].time, 100)
        self.assertEqual(sorted_data_without_bot_comments["1"][0].text, "d")
        self.assertEqual(sorted_data_without_bot_comments["1"][1].time, 200)
        self.assertEqual(sorted_data_without_bot_comments["1"][1].text, "a")
        self.assertEqual(sorted_data_without_bot_comments["1"][2].time, 300)
        self.assertEqual(sorted_data_without_bot_comments["1"][2].text, "b")
        self.assertEqual(all_number_of_bot_comments, 3)
    def test_process_data_when_all_bots(self):
        self.data1[0]["unixReviewTime"] = 300
        (
            sorted_data_without_bot_comments,
            all_number_of_bot_comments,
        ) = analyze_bots_comments([self.data1, self.data2])
        self.assertCountEqual(sorted_data_without_bot_comments.keys(), [])
        self.assertEqual(all_number_of_bot_comments, 6)
    def test_process_data_without_bots(self):
        self.data1[0]["unixReviewTime"] = 200
        self.data1[1]["unixReviewTime"] = 300
        (
            sorted_data_without_bot_comments,
            all_number_of_bot_comments,
        ) = analyze_bots_comments([self.data1, self.data2])
        self.assertCountEqual(sorted_data_without_bot_comments.keys(), ["1", "2"])
        self.assertEqual(all_number_of_bot_comments, 0)

class TestGetNearestReviews(TestCase):
    def setUp(self):
        self.data1 = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 200,},
            {"reviewerID": "2", "reviewText": "e", "unixReviewTime": 500},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 400},
        ]
        self.data2 = [
            {"reviewerID": "1", "reviewText": "b", "unixReviewTime": 400},
            {"reviewerID": "1", "reviewText": "d", "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 500},
            {"reviewerID": "3", "reviewText": None, "unixReviewTime": 10},
        ]
    def test_get_nearest_reviews_with_bots(self):
        nearest_reviews, all_number_of_bot_comments = get_nearest_reviews(
            [self.data1, self.data2]
        )
        self.assertEqual(nearest_reviews, ["1", [100, "a", "d"]])
        self.assertEqual(all_number_of_bot_comments, 3)
    def test_get_nearest_reviews_when_all_bots(self):
        self.data1[0]["unixReviewTime"] = 400
        nearest_reviews, all_number_of_bot_comments = get_nearest_reviews(
            [self.data1, self.data2]
        )
        self.assertEqual(nearest_reviews, ["", [0, "", ""]])
        self.assertEqual(all_number_of_bot_comments, 6)
        self.assertEqual(nearest_reviews[1][0] // 60 // 60 // 24, 0)
        self.assertEqual(len(nearest_reviews[1][1]), 0)
        self.assertEqual(len(nearest_reviews[1][2]), 0)

if __name__ == "__main__":
    main(verbosity=2)
