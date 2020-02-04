from source import get_data
import re
from document_creation import file_create
from operator import itemgetter


def word_list_from_positive_comment(main_dict):
    '''function returns the most popular words from positive messages

    3.1. Task_3.py: to create file words-stats1.cvs и words-stats2.cvs
    containing information about the most popular words from positive and negative messages.
    '''
    positive_comment = []
    for item in main_dict.values():
        if 'overall' in item.keys():
            if item['overall'] >= 3:
                positive_comment.append(item['reviewText'])
    positive_comment = str(positive_comment).replace("'", '')
    word_positive_comment = []
    for item in re.split(r'\W+', positive_comment):
        if len(item) > 1:
            word_positive_comment.append(item.lower())
    popular_in_positive_comment = dict.fromkeys(word_positive_comment, 0)
    for word in word_positive_comment:
        popular_in_positive_comment[word] = popular_in_positive_comment.get(word) + 1
    return popular_in_positive_comment

def word_list_from_negative_comment(main_dict):
    '''function returns the most popular words from negative messages

    3.2. Task_3.py: to create file words-stats1.cvs и words-stats2.cvs
    containing information about the most popular words from positive and negative messages.
    '''
    negative_comment = []
    for item in main_dict.values():
        if 'overall' in item.keys():
            if item['overall'] < 3:
                negative_comment.append(item['reviewText'])
    negative_comment = str(negative_comment).replace("'", '')
    word_negative_comment = []
    for item in re.split(r'\W+', negative_comment):
        if len(item) > 1:
            word_negative_comment.append(item.lower())
    popular_in_negative_comment = dict.fromkeys(word_negative_comment, 0)
    for word in word_negative_comment:
        popular_in_negative_comment[word] = popular_in_negative_comment.get(word) + 1
    return popular_in_negative_comment


if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    data = word_list_from_positive_comment(main_dict)
    file_create().save_file('words-stats1.cvs', sorted(data.items(), key=itemgetter(1), reverse=True))
    data = word_list_from_negative_comment(main_dict)
    file_create().save_file('words-stats2.cvs', sorted(data.items(), key=itemgetter(1), reverse=True))