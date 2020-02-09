from source.get_data import get_data
from itertools import groupby
from document_creation import save_file
from common_functions import asins_value, avg_overall
import asyncio
from time import time


def best_comment(main_dict):
    '''function returns the messages with the most “likes” and the application (asin) associated with it

    1.2. Task_1.py: to create file general-stats.cvs containing information about
    messages with the most “likes” from the entire data set and the application (asin) associated with it;
    '''
    best_comment = max(main_dict, key=lambda review: review['helpful'][0])
    comment = [
        ['Messages with the most “likes” from the entire data set and the application (asin) associated with it:'],
        ['like:', best_comment['helpful'][0]],
        ['asin:', best_comment['asin']],
        ['reviewText:', best_comment['reviewText']]
    ]
    return comment


def count_deltatime(reviews):
    '''function returns information per user about the two nearest reviews were sent by this user.'''

    min_deltatime = min([[reviews[i]['unixReviewTime'] - reviews[i-1]['unixReviewTime'],
                          reviews[i]['reviewText'], reviews[i-1]['reviewText']]
                        if len(reviews) > 1 else ['single_review', reviews['reviewText'], '']
                        for i in range(1, len(reviews))],
                        key=lambda deltatime: deltatime[0])

    return min_deltatime


def nearest_reviews(main_dict):
    '''function returns the shortest interval between reviews of one user and the length of both messages.

    Task_1.py: to create file general-stats.cvs containing information about
    the shortest interval between ratings of one user (among all users) and
    the length of both messages which create this interval;

    It is assumed that a user who leaves several reviews per second may be a automatic bot.
    Reviews were sent by such users aren't analyze.
    '''

    unix_diff_per_name = {
        reviewID: count_deltatime(sorted(reviews, key=lambda review: review['unixReviewTime']))
        for reviewID, reviews
        in groupby(sorted(main_dict, key=lambda review: review['reviewerID']),
                   key=lambda review: review['reviewerID'])
    }

    nearest_comments = min(
        dict(filter(lambda review: review[1][0] != 0 and review[1][0] != 'single_review', unix_diff_per_name.items())).items(),
        key=lambda review: review[1][0]
    )


    number_of_single_comments = len(dict(filter(lambda review: review[1][0] == 'single_review', unix_diff_per_name.items())))
    potential_bot = set([reviewerID for reviewerID in dict(filter(lambda review: review[1][0] == 0, unix_diff_per_name.items())).keys()])
    number_of_bot_comments = sum([len(list(reviews)) for reviewID, reviews in groupby(sorted(main_dict, key=lambda review: review['reviewerID']),
                   key=lambda review: review['reviewerID']) if reviewID in potential_bot])
    number_unanalyzed_reviews = number_of_single_comments + number_of_bot_comments

    comment = [
        ['The shortest interval between ratings of one user (among all users) '
            'and the length of both messages which create this interval:'],
        ['interval = ', '{} days {} hour {} min {} sec;'.format(
            nearest_comments[1][0] // 60 // 60 // 24,
            nearest_comments[1][0] // 60 // 60 % 24,
            nearest_comments[1][0] // 60 % 60 % 24,
            nearest_comments[1][0] % 60 % 60 % 24)],
        ['lenght comment_1:', len(nearest_comments[1][1])],
        ['lenght comment_2:', len(nearest_comments[1][2])]
    ]

    return comment, number_unanalyzed_reviews

def bad_comment(main_dict):
    '''function returns the application which received the most useless message

    1.3. Task_1.py: to create file general-stats.cvs containing information about
    the application which received the most useless message;
    '''
    bad_comment = min(
        list(filter(lambda review: review['helpful'][1] != 0, main_dict)),
        key=lambda review: review['helpful'][0]/review['helpful'][1]
    )
    comment = [
        ['The application which received the most useless message:'],
        ['helpfulness:', '{}%'.format(bad_comment['helpful'][0]/bad_comment['helpful'][1]*100)],
        ['asin:', bad_comment['asin']],
        ['reviewText:', bad_comment['reviewText']]
    ]
    return comment

def nonanalys_data(main_dict, count_analyzed_review = 0):
    '''function returns the number of records that cannot be processed for every point above.

    1.5. Task_1.py: to create file general-stats.cvs containing information about
    the number of records that cannot be processed for every point above.
    '''
    comment = [['The number of records that cannot be processed: ']]

    count_unanalyzed_1 = 0
    for item in main_dict:
        if not 'asin' in item.keys() or not 'overall' in item.keys():
            count_unanalyzed_1 += 1
    comment.append([count_unanalyzed_1, ' - for average rating (overall) of each application (asin)'])

    count_unanalyzed_2 = 0
    for item in main_dict:
        if not 'asin' in item.keys() or not 'helpful' in item.keys() or not 'reviewText' in item.keys():
            count_unanalyzed_2 += 1
    comment.append([count_unanalyzed_2, ' - to get the application which received the most useless message'])

    count_unanalyzed_3 = len(main_dict) - count_analyzed_review
    comment.append(['{} or {}%'.format(count_unanalyzed_3, round(count_unanalyzed_3/len(main_dict) * 100)),
                    ' - to get the shortest interval between ratings of one user (among all users) '
                    'and the length of both messages which create this interval;'])

    count_unanalyzed_4 = count_unanalyzed_2
    for item in main_dict:
        if item['helpful'][1] == 0:
            count_unanalyzed_4 += 1
    comment.append(['{} or {}%'.format(count_unanalyzed_4, round(count_unanalyzed_4/len(main_dict) * 100)),
                    ' - to get the application which received the most useless message'])
    return comment


if __name__ == "__main__":
    data1, data2 = get_data('Apps_for_Android_5.json')
    file_name = 'general-stats.cvs'
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(asins_value(data1)), ioloop.create_task(asins_value(data2))]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
    asins_value = tasks[1].result()
    save_file(file_name, [[value[0], value[1]] for value in avg_overall(asins_value)])
    # save_file(file_name, best_comment(main_dict), 'a')
    # comment_1, number_unanalyzed_reviews_1 = nearest_reviews(main_dict)
    # save_file(file_name, comment_1, 'a')
    # save_file(file_name, bad_comment(main_dict), 'a')
    # save_file(file_name, nonanalys_data(main_dict, number_unanalyzed_reviews_1), 'a')