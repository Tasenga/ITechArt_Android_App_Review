from os import walk
from os.path import dirname, abspath, join
from common_module.work_with_document import get_data_from_json, save_file
import re
from collections import Counter
from operator import itemgetter
from concurrent.futures import ProcessPoolExecutor


def split_text_up(text):
    """function gets a text and returns list of words from this text"""
    list_of_words = []
    for review in text:
        list_of_words.extend(re.split(r"\W+", review.replace("'", "_").lower()))
    return list_of_words

def popular_word_list(words_list):
    """function returns the words from word_list with number of using per word"""
    number_of_words = Counter(list(sorted(filter(lambda word: word != "", words_list))))
    return number_of_words

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

def get_lists_of_popular_word_parallel(*args):
    result_list_for_positive_comment = {}
    result_list_for_negative_comment = {}
    with ProcessPoolExecutor() as executor:
        for result in executor.map(get_list_of_popular_word, args):
            for word, count_word in dict(result[0]).items():
                count = result_list_for_positive_comment.get(word, 0)
                result_list_for_positive_comment[word] = count + count_word
            for word, count_word in dict(result[1]).items():
                count = result_list_for_negative_comment.get(word, 0)
                result_list_for_negative_comment[word] = count + count_word
        return result_list_for_positive_comment, result_list_for_negative_comment


if __name__ == "__main__":

    documents = []
    for root, dir, files in walk(join(dirname(abspath(__file__)), "source", "data")):
        for name in files:
            documents.append(join(root, name))

    data = []
    with ProcessPoolExecutor() as executor:
        for part_of_data in executor.map(get_data_from_json, documents):
            data.extend(part_of_data)

    result_list_for_positive_comment, result_list_for_negative_comment = get_lists_of_popular_word_parallel(data)

    save_file(
        "FP_analysis_of_reviews_from_Amazon",
        "words-stats1.cvs",
        sorted(
            result_list_for_positive_comment.items(), key=itemgetter(1), reverse=True
        ),
    )
    save_file(
        "FP_analysis_of_reviews_from_Amazon",
        "words-stats2.cvs",
        sorted(
            result_list_for_negative_comment.items(), key=itemgetter(1), reverse=True
        ),
    )
