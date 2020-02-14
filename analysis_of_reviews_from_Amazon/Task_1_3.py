from source.get_data import get_data
import re
from document_creation import save_file
from operator import itemgetter
from time import time


def get_text(main_dict, overall_values):
    '''function gets a text and returns list of reviews in depends on overall values'''
    message_list = [item['reviewText'] for item in main_dict
                    if 'overall' in item.keys() and item['overall'] in overall_values]
    return message_list

def split_text_up(text):
    '''function gets a text and returns list of words from this text'''
    list_of_words = []
    for review in text:
        list_of_words.extend(re.split(r'\W+', review.replace("'", '_').lower()))
    return list_of_words

def popular_word_list(words_list):
    '''function returns the most popular words from word_list

    3.1. Task_3.py: to create file words-stats1.cvs и words-stats2.cvs
    containing information about the most popular words from positive and negative messages.
    '''
    popular_in_positive_comment = {}
    for word in words_list:
        if word != '':
            count = popular_in_positive_comment.get(word, 0)
            popular_in_positive_comment[word] = count + 1
    return popular_in_positive_comment


if __name__ == "__main__":
    main_dict = get_data('Apps_for_Android_5.json')

    words_in_positive_comments = popular_word_list(split_text_up(get_text(main_dict, range(4, 6))))
    save_file('words-stats1.cvs',
                            sorted(words_in_positive_comments.items(), key=itemgetter(1), reverse=True))
    words_in_negative_comments = popular_word_list(split_text_up(get_text(main_dict, range(1, 4))))
    save_file('words-stats2.cvs',
                            sorted(words_in_negative_comments.items(), key=itemgetter(1), reverse=True))
