from unittest import TestCase, main
from Task_9_1 import best_comment, bad_comment, nonanalys_data, total_nonanalys_data


class TestBestComment(TestCase):
    def test_basic_work(self):
        data = [
            {
                "asin": "B006OCM13M",
                "helpful": [1, 1],
                "reviewText": "Don't _!@#$%^&*()_/*"
            },
            {
                "asin": "B006OCM13M",
                "helpful": [0, 0],
                "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000."
            },
            {
                "asin": "B006OCM13M",
                "helpful": [4, 5],
                "reviewText": "",
            }
        ]
        self.assertEqual(best_comment(data), data[2])
    def test_empty_input(self):
        best_review = best_comment([])
        self.assertEqual(
            best_review, {"asin": None, "helpful": [None, None], "reviewText": None}
        )
        self.assertIsNotNone(best_review)

class TestBadComment(TestCase):
    def test_basic_work(self):
        data = [
            {
                "asin": "B006OCM13M",
                "helpful": [1, 1],
                "reviewText": "Don't _!@#$%^&*()_/*"
            },
            {
                "asin": "B006OCM13M",
                "helpful": [0, 0],
                "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000."
            },
            {
                "asin": "B006OCM13M",
                "helpful": [4, 5],
                "reviewText": "",
            }
        ]
        self.assertEqual(bad_comment(data), data[2])
    def test_empty_input(self):
        bad_review = bad_comment([])
        self.assertEqual(
            bad_review, {"asin": None, "helpful": [float("inf"), 1], "reviewText": None}
        )
        comment = [
            bad_review["helpful"][0] / bad_review["helpful"][1],
            bad_review["asin"],
            bad_review["reviewText"],
        ]
        self.assertIsNotNone(comment)
    def test_division_zero(self):
        data = [
            {
                "reviewerID": "A6RO7271EKVXO",
                "asin": "B006OCM13M",
                "helpful": [0, 0],
                "reviewText": "000000000000000",
                "overall": 4.0,
                "summary": "fun",
                "unixReviewTime": 1355875200,
                "reviewTime": "01 17, 2013",
            },
            {
                "reviewerID": "A2XOJXOT0AFXHE",
                "asin": "B00724WGQS",
                "reviewerName": "Vesta Gleissner",
                "helpful": [0, 0],
                "reviewText": "",
                "overall": 4.0,
                "summary": "200,000 Free Quotes",
                "unixReviewTime": 1357862400,
                "reviewTime": "01 11, 2013",
            }
        ]
        self.assertEqual(
            bad_comment(data),
            {"asin": None, "helpful": [float("inf"), 1], "reviewText": None},
        )

class TestNonanalysData(TestCase):
    def test_basic_work(self):
        self.assertEqual(
            nonanalys_data(
                [
                    {
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "reviewText": "Don't _!@#$%^&*()_/*",
                        "overall": 1.0
                    },
                    {
                        "asin": "B006OCM13M",
                        "helpful": [0, 0],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                        "overall": 5.0
                    }
                ]
            ),
            (0, 0, 1))
        self.assertEqual(
            nonanalys_data(
                [
                    {
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "reviewText": "Don't _!@#$%^&*()_/*",
                        "overall": 1.0
                    },
                    {
                        "helpful": [0, 0],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                        "overall": 5.0
                    }
                ]
            ),
            (1, 1, 1))
        self.assertEqual(
            nonanalys_data(
                [
                    {
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "overall": 1.0
                    },
                    {
                        "helpful": [0, 0],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                        "overall": 5.0
                    }
                ]
            ),
            (1, 2, 2))
        self.assertEqual(
            nonanalys_data(
                [
                    {
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "reviewText": "Don't _!@#$%^&*()_/*",
                        "overall": 1.0
                    },
                    {
                        "asin": "B006OCM13M",
                        "helpful": [4, 5],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                    }
                ]
            ),
            (1, 0, 0))

class TestTotalNonanalysData(TestCase):
    def test_basic_work(self):
        self.assertEqual(
            total_nonanalys_data(
                    [[{
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "reviewText": "Don't _!@#$%^&*()_/*",
                        "overall": 1.0
                    }],
                    [{
                        "asin": "B006OCM13M",
                        "helpful": [0, 0],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                        "overall": 5.0
                    }]]
            ),
            (0, 0, 1))
        self.assertEqual(
            total_nonanalys_data(
                [
                    [{
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "reviewText": "Don't _!@#$%^&*()_/*",
                        "overall": 1.0
                    }],
                    [{
                        "helpful": [0, 0],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                        "overall": 5.0
                    }]
                ]
            ),
            (1, 1, 1))
        self.assertEqual(
            total_nonanalys_data(
                [
                    [{
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "overall": 1.0
                    }],
                    [{
                        "helpful": [0, 0],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                        "overall": 5.0
                    }]
                ]
            ),
            (1, 2, 2))
        self.assertEqual(
            total_nonanalys_data(
                [
                    [{
                        "asin": "B006OCM13M",
                        "helpful": [1, 1],
                        "reviewText": "Don't _!@#$%^&*()_/*",
                        "overall": 1.0
                    }],
                    [{
                        "asin": "B006OCM13M",
                        "helpful": [4, 5],
                        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
                    }]
                ]
            ),
            (1, 0, 0))

if __name__ == "__main__":
    main(verbosity=2)
