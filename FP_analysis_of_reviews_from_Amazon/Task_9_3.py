from os.path import dirname, abspath
from pathlib import Path
from common_module.work_with_document import get_data_from_json, save_file
import re
from collections import Counter
from operator import itemgetter
from concurrent.futures import ProcessPoolExecutor
from common_functions import run_func_parallel


def split_text_up(text):
    """function gets a text and returns list of words from this text"""
    list_of_words = []
    for review in text:
        list_of_words.extend(re.split(r"\W+", review.replace("'", "_").lower()))
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

    positive_message_list = tuple(
        map(
            lambda review: review["reviewText"],
            tuple(filter(lambda review: review["overall"] >= 4, data)),
        )
    )
    negative_message_list = tuple(
        map(
            lambda review: review["reviewText"],
            tuple(filter(lambda review: review["overall"] < 4, data)),
        )
    )
    list_of_words_in_positive_comment = split_text_up(positive_message_list)

    list_of_words_in_negative_comment = split_text_up(negative_message_list)

    number_of_words_in_positive_comment = popular_word_list(
        list_of_words_in_positive_comment
    )

    number_of_words_in_negative_comment = popular_word_list(
        list_of_words_in_negative_comment
    )

    return number_of_words_in_positive_comment, number_of_words_in_negative_comment

def create_list_word(list_of_word={}):
    count = list_of_word.get(word, 0)
    list_of_word[word] = count + count_word
    return list_of_word



if __name__ == "__main__":

    chunks = Path(dirname(abspath(__file__)), "source", "data").iterdir()
    with ProcessPoolExecutor() as executor:
        data = [it for it in executor.map(get_data_from_json, chunks)]

    list_for_positive_comment = {}
    list_for_negative_comment = {}
    for result in run_func_parallel(get_list_of_popular_word, data):
        for word, count_word in dict(result[0]).items():
            list_for_positive_comment = create_list_word(list_for_positive_comment)
        for word, count_word in dict(result[1]).items():
            list_for_negative_comment = create_list_word(list_for_negative_comment)

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
