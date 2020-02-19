from unittest import TestCase, main
from copy import deepcopy as dc
from Task_9_1 import best_comment, bad_comment, nonanalys_data, total_nonanalys_data

DATA = [
    {
        "reviewerID": "A6RO7271EKVXO",
        "asin": "B006OCM13M",
        "reviewerName": "Snoohz",
        "helpful": [1, 1],
        "reviewText": "Don't _!@#$%^&*()_/*",
        "overall": 1.0,
        "unixReviewTime": 1355875200,
        "reviewTime": "01 17, 2013",
    },
    {
        "reviewerID": "AVD9TN3YMFBAI",
        "asin": "B006OCM13M",
        "helpful": [0, 1],
        "reviewText": "My whole family (hubby, I, and kids)... a..aaaa 0000000.",
        "overall": 5.0,
        "unixReviewTime": 1359072000,
        "reviewTime": "01 17, 2013",
    },
    {
        "reviewerID": "AVD9TN3YMFBAI",
        "asin": "B006OCM13M",
        "reviewerName": "Snoohz",
        "helpful": [4, 5],
        "reviewText": "",
        "overall": 5.0,
        "unixReviewTime": 1350604800,
        "reviewTime": "01 17, 2013",
    },
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
    },
    {
        "reviewerID": "AVD9TN3YMFBAI",
        "asin": "B006OCM13M",
        "reviewerName": "Snoohz",
        "helpful": [1, 5],
        "reviewText": "AAAA!!!tic_toc",
        "overall": 5.0,
        "unixReviewTime": 1380604800,
        "reviewTime": "01 17, 2013",
    },
]

class TestBestComment(TestCase):
    def setUp(self):
        self.data = dc(DATA)
    def test_basic_work(self):
        self.assertEqual(best_comment(self.data), self.data[2])
    def test_empty_input(self):
        best_review = best_comment([])
        self.assertEqual(
            best_review, {"asin": None, "helpful": [None, None], "reviewText": None}
        )
        self.assertIsNone(best_review["helpful"][0])
        self.assertIsNone(best_review["asin"])
        self.assertIsNone(best_review["reviewText"])

class TestBadComment(TestCase):
    def setUp(self):
        self.data = dc(DATA)
    def test_basic_work(self):
        self.assertEqual(bad_comment(self.data), self.data[1])
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
        data = [item for item in self.data if item["helpful"][1] == 0]
        self.assertEqual(
            bad_comment(data),
            {"asin": None, "helpful": [float("inf"), 1], "reviewText": None},
        )

class TestNonanalysData(TestCase):
    def setUp(self):
        self.data = dc(DATA)
    def test_basic_work(self):
        self.assertEqual(nonanalys_data(self.data), (0, 0, 2))
        self.data[0].pop("asin")
        self.assertEqual(nonanalys_data(self.data), (1, 1, 2))
        self.data[0].pop("overall")
        self.assertEqual(nonanalys_data(self.data), (1, 1, 2))
        self.data[1].pop("overall")
        self.assertEqual(nonanalys_data(self.data), (2, 1, 2))
        self.data[2].pop("reviewText")
        self.assertEqual(nonanalys_data(self.data), (2, 2, 2))
        self.data[0]["helpful"][1] = 0
        self.assertEqual(nonanalys_data(self.data), (2, 2, 3))
        self.data[0]["helpful"][1] = 1
        self.data[3]["helpful"][1] = 1
        self.assertEqual(nonanalys_data(self.data), (2, 2, 1))

class TestTotalNonanalysData(TestCase):
    def setUp(self):
        self.data1 = dc(DATA[0:3])
        self.data2 = dc(DATA[3:6])
    def test_basic_work(self):
        self.assertEqual(total_nonanalys_data([self.data1, self.data2]), (0, 0, 2))
        self.data1[0].pop("asin")
        self.assertEqual(total_nonanalys_data([self.data1, self.data2]), (1, 1, 2))
        self.data1[0].pop("overall")
        self.assertEqual(total_nonanalys_data([self.data1, self.data2]), (1, 1, 2))
        self.data1[1].pop("overall")
        self.assertEqual(total_nonanalys_data([self.data1, self.data2]), (2, 1, 2))
        self.data1[2].pop("reviewText")
        self.assertEqual(total_nonanalys_data([self.data1, self.data2]), (2, 2, 2))
        self.data1[0]["helpful"][1] = 0
        self.assertEqual(total_nonanalys_data([self.data1, self.data2]), (2, 2, 3))
        self.data1[0]["helpful"][1] = 1
        self.data2[0]["helpful"][1] = 1
        self.assertEqual(total_nonanalys_data([self.data1, self.data2]), (2, 2, 1))

if __name__ == "__main__":
    main(verbosity=2)
