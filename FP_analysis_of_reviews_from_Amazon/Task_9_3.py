from os.path import dirname, abspath, join
from pathlib import Path
from common_module.work_with_document import get_data_from_json, save_file
import re
from collections import Counter
from operator import itemgetter
from itertools import groupby
from itertools import chain
from common_functions import run_func_parallel


def text_to_words(text):
    """function gets a text and returns list of words from this text"""
    return re.split(r"\W+", text.replace("'", "_").lower())

def create_words_counter(comments):
    return Counter(
        [
            word
            for word
            in chain.from_iterable([text_to_words(comment) for comment in comments])
            if word != ""
        ]
    )

def get_list_of_popular_word(data):
    """common function which returns the dictionaries with words and number of using per word
    from positive and negative messages.

    3.1. Task_9_3.py: to create file words-stats1.cvs и words-stats2.cvs
    containing information about the most popular words from positive and negative messages.
    """
    comment_words_by_sentiment = {
        sentiment: create_words_counter([review["reviewText"] for review in reviews])
        for sentiment, reviews in groupby(
            sorted(
                data, key=lambda review: review["overall"]
            ),
            key=lambda review: review["overall"] >= 4)
    }
    return (
        comment_words_by_sentiment[True],  # number of words in positive comment
        comment_words_by_sentiment[False]  # number of words in negative comment
    )

def analyze_popular_words_by_sentiment(data):
    total_positive = Counter()
    total_negative = Counter()
    for positive, negative in run_func_parallel(get_list_of_popular_word, data):
        total_positive += positive
        total_negative += negative
    return total_positive, total_negative


if __name__ == "__main__":

    chunks = Path(dirname(abspath(__file__)), "source", "data").iterdir()
    data = run_func_parallel(get_data_from_json, chunks)

    # path_to_save
    Path(join(dirname(abspath(__file__)), "resulting data")).mkdir(parents=True, exist_ok=True)
    path_to_save = Path(join(dirname(abspath(__file__)), "resulting data"))

    list_for_positive_comment, list_for_negative_comment = analyze_popular_words_by_sentiment(data)

    save_file(
        path_to_save,
        "words-stats1.cvs",
        sorted(
            list_for_positive_comment.items(), key=itemgetter(1), reverse=True
        ),
    )
    save_file(
        path_to_save,
        "words-stats2.cvs",
        sorted(
            list_for_negative_comment.items(), key=itemgetter(1), reverse=True
        ),
    )
