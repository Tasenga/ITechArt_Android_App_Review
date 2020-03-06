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
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 200},
            {"reviewerID": "1", "reviewText": "b", "unixReviewTime": 300},
            {"reviewerID": "1", "reviewText": None, "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 500},
        ]
    def test_basic_work(self):
        self.assertIsInstance(prepare_data(self.data), dict)
        self.assertEqual(
            prepare_data(self.data),
            {
                "1": [
                    ReviewTimeInfo(time=100, text=None),
                    ReviewTimeInfo(time=200, text="a"),
                    ReviewTimeInfo(time=300, text="b"),
                ],
                "2": [ReviewTimeInfo(time=500, text="f")],
            },
        )
        self.assertTrue(
            all(
                isinstance(i.text, str) or i.text is None
                for v in prepare_data(self.data).values()
                for i in v
            )
        )

class TestCountDeltatime(TestCase):
    def test_count_deltatime(self):
        data1 = [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")]
        data2 = [
            ReviewTimeInfo(100, None),
            ReviewTimeInfo(200, "c"),
            ReviewTimeInfo(400, "d"),
        ]
        self.assertEqual(count_deltatime(data1), [0, "b", "a"])
        self.assertEqual(count_deltatime(data2), [100, "c", None])
    def test_count_deltatime_with_unsorted_unixtime(self):
        data = [ReviewTimeInfo(400, None), ReviewTimeInfo(300, "c")]
        with self.assertRaises(Exception):
            count_deltatime(data)

class TestGetUnixDiffPerName(TestCase):
    def test_get_unix_diff_per_name(self):
        data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")],
            "2": [
                ReviewTimeInfo(100, None),
                ReviewTimeInfo(200, "c"),
                ReviewTimeInfo(400, "d"),
            ],
            "3": [ReviewTimeInfo(200, None)],
        }
        self.assertEqual(
            get_unix_diff_per_name(data),
            [
                ["1", [0, "b", "a"]],
                ["2", [100, "c", None]],
                ["3", ["single_review", "single_review", "single_review"]],
            ],
        )

class TestGetPotentialBots(TestCase):
    def test_get_potential_bots(self):
        data = [
            ["1", [0, "b", "c"]],
            ["2", [100, "d", "c"]],
            ["3", ["single_review", "single_review", "single_review"]],
            ["4", [0, "e", "f"]],
        ]
        self.assertCountEqual(get_potential_bots(data), {"1", "4", None})
        self.assertCountEqual(get_potential_bots(), set())
        self.assertCountEqual(get_potential_bots([["1", [100, "b", "c"]]]), {None})

class TestFilterBotReview(TestCase):
    def test_filter_bot_review_basic_work(self):
        data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")],
            "2": [
                ReviewTimeInfo(100, None),
                ReviewTimeInfo(300, "c"),
                ReviewTimeInfo(400, "d"),
            ],
            "3": [ReviewTimeInfo(200, None)],
        }
        bots = {"1", None}
        analyzed_data, number_of_bot_comments = filter_bot_review(data, bots)
        self.assertEqual(number_of_bot_comments, 2)
        self.assertEqual(
            analyzed_data,
            {
                "2": [
                    ReviewTimeInfo(time=100, text=None),
                    ReviewTimeInfo(time=300, text="c"),
                    ReviewTimeInfo(time=400, text="d"),
                ],
                "3": [ReviewTimeInfo(time=200, text=None),],
            },
        )
        self.assertIsInstance(analyzed_data, dict)
        self.assertTrue(
            all(
                isinstance(i.text, str) or i.text is None
                for v in analyzed_data.values()
                for i in v
            )
        )
    def test_filter_bot_review_without_bots(self):
        data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(200, "b")],
            "2": [ReviewTimeInfo(100, None)],
        }
        analyzed_data, number_of_bot_comments = filter_bot_review(data, set())
        self.assertEqual(number_of_bot_comments, 0)
        self.assertEqual(
            analyzed_data,
            {
                "1": [
                    ReviewTimeInfo(time=100, text="a"),
                    ReviewTimeInfo(time=200, text="b"),
                ],
                "2": [ReviewTimeInfo(time=100, text=None)],
            },
        )

        analyzed_data, number_of_bot_comments = filter_bot_review(data, {None})
        self.assertEqual(number_of_bot_comments, 0)
        self.assertEqual(
            analyzed_data,
            {
                "1": [
                    ReviewTimeInfo(time=100, text="a"),
                    ReviewTimeInfo(time=200, text="b"),
                ],
                "2": [ReviewTimeInfo(time=100, text=None)],
            },
        )
    def test_filter_bot_review_when_all_bots(self):
        data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")],
            "2": [ReviewTimeInfo(100, None), ReviewTimeInfo(100, None)],
        }
        bots = {"1", "2", None}
        analyzed_data, number_of_bot_comments = filter_bot_review(data, bots)
        self.assertEqual(number_of_bot_comments, 4)
        self.assertEqual(analyzed_data, {})

class TestProcessData(TestCase):
    def test_process_data_with_bots(self):
        data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(100, "b")],
            "2": [
                ReviewTimeInfo(100, None),
                ReviewTimeInfo(300, "c"),
                ReviewTimeInfo(400, "d"),
            ],
            "3": [ReviewTimeInfo(200, None)],
        }
        analyzed_data, potential_bots, number_of_bot_comments = process_data(data)
        self.assertEqual(
            analyzed_data,
            {
                "2": [
                    ReviewTimeInfo(100, None),
                    ReviewTimeInfo(300, "c"),
                    ReviewTimeInfo(400, "d"),
                ],
                "3": [ReviewTimeInfo(200, None)],
            },
        )
        self.assertEqual(potential_bots, {"1", None})
        self.assertEqual(number_of_bot_comments, 2)
        self.assertIsInstance(analyzed_data, dict)
    def test_process_data_without_bots(self):
        data = {
            "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(300, "b")],
            "2": [
                ReviewTimeInfo(100, None),
                ReviewTimeInfo(300, "c"),
                ReviewTimeInfo(400, "d"),
            ],
            "3": [ReviewTimeInfo(200, None)],
        }
        analyzed_data, potential_bots, number_of_bot_comments = process_data(data)
        self.assertEqual(
            analyzed_data,
            {
                "1": [ReviewTimeInfo(100, "a"), ReviewTimeInfo(300, "b")],
                "2": [
                    ReviewTimeInfo(100, None),
                    ReviewTimeInfo(300, "c"),
                    ReviewTimeInfo(400, "d"),
                ],
                "3": [ReviewTimeInfo(200, None)],
            },
        )
        self.assertEqual(potential_bots, {None})
        self.assertEqual(number_of_bot_comments, 0)

class TestAnalyzeBotsComments(TestCase):
    def test_analyze_bots_comments_with_bots(self):
        data1 = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 200},
            {"reviewerID": "2", "reviewText": "e", "unixReviewTime": 500},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 400},
        ]
        data2 = [
            {"reviewerID": "1", "reviewText": "b", "unixReviewTime": 300},
            {"reviewerID": "1", "reviewText": "d", "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 500},
        ]
        (
            sorted_data_without_bot_comments,
            all_number_of_bot_comments,
        ) = analyze_bots_comments([data1, data2])
        self.assertEqual(
            sorted_data_without_bot_comments,
            {
                "1": [
                    ReviewTimeInfo(100, "d"),
                    ReviewTimeInfo(200, "a"),
                    ReviewTimeInfo(300, "b"),
                ]
            },
        )
        self.assertIsInstance(sorted_data_without_bot_comments, dict)
        self.assertEqual(all_number_of_bot_comments, 3)
    def test_analyze_bots_comments_when_all_bots(self):
        data1 = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "e", "unixReviewTime": 500},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 400},
        ]
        data2 = [
            {"reviewerID": "1", "reviewText": "b", "unixReviewTime": 300},
            {"reviewerID": "1", "reviewText": "d", "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 500},
        ]
        (
            sorted_data_without_bot_comments,
            all_number_of_bot_comments,
        ) = analyze_bots_comments([data1, data2])
        self.assertEqual(sorted_data_without_bot_comments, {})
        self.assertEqual(all_number_of_bot_comments, 6)
    def test_analyze_bots_comments_without_bots(self):
        data1 = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 200},
            {"reviewerID": "2", "reviewText": "e", "unixReviewTime": 300},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 400},
        ]
        data2 = [
            {"reviewerID": "1", "reviewText": "b", "unixReviewTime": 300},
            {"reviewerID": "1", "reviewText": "d", "unixReviewTime": 100},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 500},
        ]
        (
            sorted_data_without_bot_comments,
            all_number_of_bot_comments,
        ) = analyze_bots_comments([data1, data2])
        self.assertEqual(
            sorted_data_without_bot_comments,
            {
                "1": [
                    ReviewTimeInfo(100, "d"),
                    ReviewTimeInfo(200, "a"),
                    ReviewTimeInfo(300, "b"),
                ],
                "2": [
                    ReviewTimeInfo(300, "e"),
                    ReviewTimeInfo(400, "f"),
                    ReviewTimeInfo(500, "f"),
                ],
            },
        )
        self.assertEqual(all_number_of_bot_comments, 0)

class TestGetNearestReviews(TestCase):
    def setUp(self):
        self.data1 = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 200},
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
        data1 = [
            {"reviewerID": "1", "reviewText": "a", "unixReviewTime": 400},
            {"reviewerID": "2", "reviewText": "e", "unixReviewTime": 500},
            {"reviewerID": "2", "reviewText": "f", "unixReviewTime": 400},
        ]
        nearest_reviews, all_number_of_bot_comments = get_nearest_reviews(
            [data1, self.data2]
        )
        self.assertEqual(nearest_reviews, ["", [0, "", ""]])
        self.assertEqual(all_number_of_bot_comments, 6)
        self.assertEqual(nearest_reviews[1][0] // 60 // 60 // 24, 0)

if __name__ == "__main__":
    main(verbosity=2)
