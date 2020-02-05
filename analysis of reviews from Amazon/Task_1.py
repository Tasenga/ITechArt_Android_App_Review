from source import get_data
from operator import itemgetter
from itertools import groupby
from document_creation import save_file
from collections import Counter


def avg_rating(main_dict):
    '''function returns an average rating (overall) of each application (asin)

    1.1. Task_1.py: to create file general-stats.cvs containing information about
    average rating (overall) of each application (asin);
    '''
    asins_value = {}
    for item in main_dict.values():
        overall, count = asins_value.get(item['asin'], [0, 0])
        asins_value[item['asin']] = [overall + item['overall'], count + 1]
    avg_overall = [[key, '{}'.format(round(value[0] / value[1], 2)).replace('.', ','), value[1]]
                   for key, value in asins_value.items()]
    return avg_overall

def best_comment(main_dict):
    '''function returns the messages with the most “likes” and the application (asin) associated with it

    1.2. Task_1.py: to create file general-stats.cvs containing information about
    messages with the most “likes” from the entire data set and the application (asin) associated with it;
    '''
    best_comment = max(main_dict.values(), key=lambda review: review['helpful'][0])
    comment = [
        ['Messages with the most “likes” from the entire data set and the application (asin) associated with it:'],
        ['like:', best_comment['helpful'][0]],
        ['asin:', best_comment['asin']],
        ['reviewText:', best_comment['reviewText']]
    ]
    return comment

def nearest_reviews(main_dict):
    '''function returns the shortest interval between ratings of one user and the length of both messages

    Task_1.py: to create file general-stats.cvs containing information about
    the shortest interval between ratings of one user (among all users) and
    the length of both messages which create this interval;
    '''

    analyzed_data = sorted(dict(filter(lambda review: 'reviewerName' in review[1] and 'unixReviewTime' in review[1]
                                    and review[1]['reviewerName'] != 'Amazon Customer', main_dict.items())).values(),
                                    key=lambda review: review['reviewerName'])

    unix_sorted_reviews_by_names = {
        name: sorted(reviews, key=lambda review: review['unixReviewTime'])
        for name, reviews
        in groupby((row for row in analyzed_data), key=lambda review: review['reviewerName'])
    }

    unix_max_diff_per_name = {
        name: reviews[-1]['unixReviewTime'] - reviews[0]['unixReviewTime']
        for name, reviews
        in unix_sorted_reviews_by_names.items()
        if len(reviews) > 1
    }

    global count_analyzed_data
    count_analyzed_data = len(analyzed_data)

    deltatime_between_nearest_reviews = min(
        dict(filter(lambda value: value[1] != 0, unix_max_diff_per_name.items())).values())

    len_first_comment_from_nearest = [len(unix_sorted_reviews_by_names[key][-1]['reviewText']) for key, value in
                                      unix_max_diff_per_name.items() if value == deltatime_between_nearest_reviews]
    len_second_comment_from_nearest = [len(unix_sorted_reviews_by_names[key][0]['reviewText']) for key, value in
                                      unix_max_diff_per_name.items() if value == deltatime_between_nearest_reviews]

    comment = [
        ['The shortest interval between ratings of one user (among all users) '
            'and the length of both messages which create this interval:'],
        ['interval = ', '{} hour {} min {} sec;'.format(
            deltatime_between_nearest_reviews // 60 // 60,
            deltatime_between_nearest_reviews // 60 % 60,
            deltatime_between_nearest_reviews % 60 % 60)],
        ['lenght comment_1:', len_first_comment_from_nearest[0]],
        ['lenght comment_2:', len_second_comment_from_nearest[0]]
    ]
    return comment

def bad_comment(main_dict):
    '''function returns the application which received the most useless message

    1.3. Task_1.py: to create file general-stats.cvs containing information about
    the application which received the most useless message;
    '''
    bad_comment = min(
        dict(filter(lambda review: review[1]['helpful'][1] != 0, main_dict.items())).values(),
        key=lambda review: review['helpful'][0]/review['helpful'][1]
    )
    comment = [
        ['The application which received the most useless message:'],
        ['helpfulness:', '{}%'.format(bad_comment['helpful'][0]/bad_comment['helpful'][1]*100)],
        ['asin:', bad_comment['asin']],
        ['reviewText:', bad_comment['reviewText']]
    ]
    return comment

def nonanalys_data(main_dict, count_analyzed_data):
    '''function returns the number of records that cannot be processed for every point above.

    1.5. Task_1.py: to create file general-stats.cvs containing information about
    the number of records that cannot be processed for every point above.
    '''
    comment = [['The number of records that cannot be processed: ']]

    count_unanalyzed_1 = 0
    for item in main_dict.values():
        if not 'asin' in item.keys() or not 'overall' in item.keys():
            count_unanalyzed_1 += 1
    comment.append([count_unanalyzed_1, ' - for average rating (overall) of each application (asin)'])

    count_unanalyzed_2 = 0
    for item in main_dict.values():
        if not 'asin' in item.keys() or not 'helpful' in item.keys() or not 'reviewText' in item.keys():
            count_unanalyzed_2 += 1
    comment.append([count_unanalyzed_2, ' - to get the application which received the most useless message'])

    count_unanalyzed_3 = len(main_dict) - count_analyzed_data
    comment.append(['{} or {}%'.format(count_unanalyzed_3, round(count_unanalyzed_3/len(main_dict) * 100)),
                    ' - to get the shortest interval between ratings of one user (among all users) '
                    'and the length of both messages which create this interval;'])

    count_unanalyzed_4 = count_unanalyzed_2
    for item in main_dict.values():
        if item['helpful'][1] == 0:
            count_unanalyzed_4 += 1
    comment.append(['{} or {}%'.format(count_unanalyzed_4, round(count_unanalyzed_4/len(main_dict) * 100)),
                    ' - to get the application which received the most useless message'])
    return comment


if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    count_analyzed_data = []
    file_name = 'general-stats.cvs'
    save_file(file_name, [[value[0], value[1]] for value in avg_rating(main_dict)])
    save_file(file_name, best_comment(main_dict), 'a')
    save_file(file_name, nearest_reviews(main_dict), 'a')
    save_file(file_name, bad_comment(main_dict), 'a')
    save_file(file_name, nonanalys_data(main_dict, count_analyzed_data), 'a')



