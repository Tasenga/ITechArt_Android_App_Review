from unittest import TestCase, main
from Task_9_3 import (
    text_to_words,
    create_words_counter,
    get_list_of_popular_word,
    analyze_popular_words_by_sentiment,
)
from collections import Counter

class TestTextToWords(TestCase):
    def test_text_to_words(self):
        self.assertEqual(
            text_to_words("can't...dddd a !1#$%^&(*"), ["can_t", "dddd", "a", "1", ""]
        )
    def test_text_to_words_input_none(self):
        self.assertEqual(text_to_words(""), [""])

class TestCreateWordsCounter(TestCase):
    def test_create_words_counter(self):
        self.assertEqual(
            create_words_counter(
                ["I can't...dddd a !1#$%^&(*", "I cant... 1!!! price's"]
            ),
            {"i": 2, "can_t": 1, "dddd": 1, "a": 1, "1": 2, "cant": 1, "price_s": 1},
        )

class TestGetListOfPopularWord(TestCase):
    def setUp(self):
        self.data = [
            {"reviewText": "", "overall": 1.0},
            {"reviewText": "I haven't little horse", "overall": 5.0},
            {"reviewText": None, "overall": 3.0},
            {"reviewText": "My whole  (, I, and )... a.", "overall": 4.0},
        ]
    def test_get_list_of_popular_word(self):
        self.assertEqual(
            get_list_of_popular_word(self.data),
            (
                Counter(
                    {
                        "i": 2,
                        "my": 1,
                        "whole": 1,
                        "and": 1,
                        "a": 1,
                        "haven_t": 1,
                        "little": 1,
                        "horse": 1,
                    }
                ),
                Counter(()),
            ),
        )

class TestAnalyzePopularWordsBySentiment(TestCase):
    def setUp(self):
        self.data1 = [
            {"reviewText": "", "overall": 1.0},
            {"reviewText": "I haven't little horse", "overall": 5.0},
        ]
        self.data2 = [
            {"reviewText": None, "overall": 3.0},
            {"reviewText": "My whole  (, I, and )... a.", "overall": 4.0},
        ]
    def test_analyze_popular_words_by_sentiment(self):
        self.assertEqual(
            analyze_popular_words_by_sentiment([self.data1, self.data2]),
            (
                Counter(
                    {
                        "i": 2,
                        "my": 1,
                        "whole": 1,
                        "and": 1,
                        "a": 1,
                        "haven_t": 1,
                        "little": 1,
                        "horse": 1,
                    }
                ),
                Counter(()),
            ),
        )

if __name__ == "__main__":
    main(verbosity=2)
