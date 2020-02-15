from os.path import dirname, abspath
from pathlib import Path
from common_module.work_with_document import get_data_from_json, save_file
import re
from collections import Counter
from operator import itemgetter
from itertools import groupby
from common_functions import run_func_parallel


def split_text_up(text):
    """function gets a text and returns list of words from this text"""
    list_of_words = []
    list(
        map(
            lambda review: list_of_words.extend(
                re.split(r"\W+", review.replace("'", "_").lower())
            ),
            text
        )
    )
    return list_of_words

def popular_word_list(words_list):
    """function returns the words from word_list with number of using per word"""
    return Counter(list(sorted(filter(lambda word: word != "", words_list))))

def get_list_of_popular_word(data):
    """common function which returns the dictionaries with words and number of using per word
    from positive and negative messages.

    3.1. Task_9_3.py: to create file words-stats1.cvs и words-stats2.cvs
    containing information about the most popular words from positive and negative messages.
    """
    comment_words_by_sentiment = {
        sentiment: popular_word_list(
            split_text_up([review["reviewText"] for review in reviews])
        )
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

def create_list_word(data, list_of_word={}):
    for word, count_word in data.items():
        count = list_of_word.get(word, 0)
        list_of_word[word] = count + count_word
    return list_of_word



if __name__ == "__main__":

    chunks = Path(dirname(abspath(__file__)), "source", "data").iterdir()
    data = run_func_parallel(get_data_from_json, chunks)

    list_for_positive_comment = {}
    list_for_negative_comment = {}
    for result in run_func_parallel(get_list_of_popular_word, data):
        list_for_positive_comment = create_list_word(dict(result[0]), list_for_positive_comment)
        list_for_negative_comment = create_list_word(dict(result[1]), list_for_negative_comment)

    save_file(
        Path(dirname(abspath(__file__))),
        "words-stats1.cvs",
        sorted(
            list_for_positive_comment.items(), key=itemgetter(1), reverse=True
        ),
    )
    save_file(
        Path(dirname(abspath(__file__))),
        "words-stats2.cvs",
        sorted(
            list_for_negative_comment.items(), key=itemgetter(1), reverse=True
        ),
    )
