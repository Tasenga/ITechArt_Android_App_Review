from source import get_data
import re
from document_creation import file_create
from operator import itemgetter

def message_list(main_dict):
    '''function returns positive and negative messages list'''
    positive_comments = []
    negative_comments = []
    for item in main_dict.values():
        if 'overall' in item.keys():
            if item['overall'] >= 2.5:
                positive_comments.extend(re.split(r'\W+', item['reviewText'].replace("'", '_').lower()))
            else:
                negative_comments.extend(re.split(r'\W+', item['reviewText'].replace("'", '_').lower()))
    return [positive_comments, negative_comments]

def popular_word_list(message_list):
    '''function returns the most popular words from word_list

    3.1. Task_3.py: to create file words-stats1.cvs и words-stats2.cvs
    containing information about the most popular words from positive and negative messages.
    '''
    popular_in_positive_comment = {}
    for word in message_list:
        if word != '':
            count = popular_in_positive_comment.get(word, 0)
            popular_in_positive_comment[word] = count + 1
    return popular_in_positive_comment


if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    positive_comments, negative_comments = message_list(main_dict)
    word_in_positive = popular_word_list(positive_comments)
    file_create().save_file('words-stats1.cvs', sorted(word_in_positive.items(), key=itemgetter(1), reverse=True))
    word_in_negative = popular_word_list(negative_comments)
    file_create().save_file('words-stats2.cvs', sorted(word_in_negative.items(), key=itemgetter(1), reverse=True))