from source import get_data
from itertools import groupby
from document_creation import save_file


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

def sort_dict_by_name(main_dict):
    '''function returns the sorted dictionary, where keys are ReviewerID
    and values are list of all user reviews per user

    using to complete Task_1.py: to create file general-stats.cvs containing information about
    the shortest interval between ratings of one user (among all users) and
    the length of both messages which create this interval;
    '''

    sorted_dict_by_names = {
        reviewID: sorted(reviews, key=lambda review: review['unixReviewTime'])
        for reviewID, reviews
        in groupby(sorted(main_dict.values(), key=lambda review: review['reviewerID']),
                   key=lambda review: review['reviewerID'])
    }
    return sorted_dict_by_names

def create_dict_diff_unixtime(sorted_dict):
    '''function returns the dictionary, where keys are two ReviewText (delimiter = '[delimiter]')
    and values are difference between unixReviewTime for 'reviews' in key and reviewerID who sent this reviewText

    using to complete Task_1.py: to create file general-stats.cvs containing information about
    the shortest interval between ratings of one user (among all users) and
    the length of both messages which create this interval;
    '''
    unix_diff_per_name = {
        '{}[delimiter]{}'.format(reviews[i]['reviewText'], reviews[i-1]['reviewText']):
            [reviews[i]['unixReviewTime'] - reviews[i-1]['unixReviewTime'], name]
        for name, reviews
        in sorted_dict.items()
        if len(reviews) > 1
        for i in range(len(reviews))
        if i > 1
    }
    return unix_diff_per_name

def find_potential_bots(unix_diff_per_name):
    '''function returns the set of potential bots.
    It is assumed that a potential bot may be a user who leaves several reviews per second

    using to complete Task_1.py: to create file general-stats.cvs containing information about
    the shortest interval between ratings of one user (among all users) and
    the length of both messages which create this interval;
    '''

    potential_bots = set([value[1] for value in unix_diff_per_name.values() if value[0] == 0])
    return potential_bots

def nearest_reviews(main_dict):
    '''function returns the shortest interval between reviews of one user and the length of both messages

    Task_1.py: to create file general-stats.cvs containing information about
    the shortest interval between ratings of one user (among all users) and
    the length of both messages which create this interval;
    '''

    sorted_dict = sort_dict_by_name(main_dict)
    unix_diff_per_name = create_dict_diff_unixtime(sorted_dict)
    potential_bots = find_potential_bots(unix_diff_per_name)

    # gets pure dictionary to analysis and count of reviews getting to analysis
    analyzed_dict = dict(filter(lambda review: review[0] not in potential_bots, sorted_dict.items()))
    global count_analyzed_review
    count_analyzed_review = sum([len(value) for value in analyzed_dict.values()])

    unix_diff_per_name = create_dict_diff_unixtime(analyzed_dict)

    deltatime_between_nearest_reviews = min(unix_diff_per_name.items(), key=lambda value: value[0])

    nearest_comments = [key.split('[delimiter]') for key, value in unix_diff_per_name.items()
                        if value[0] == deltatime_between_nearest_reviews[1][0]
                        and value[1] == deltatime_between_nearest_reviews[1][1]]

    comment = [
        ['The shortest interval between ratings of one user (among all users) '
            'and the length of both messages which create this interval:'],
        ['interval = ', '{} days {} hour {} min {} sec;'.format(
            deltatime_between_nearest_reviews[1][0] // 60 // 60 // 24,
            deltatime_between_nearest_reviews[1][0] // 60 // 60 % 24,
            deltatime_between_nearest_reviews[1][0] // 60 % 60 % 24,
            deltatime_between_nearest_reviews[1][0] % 60 % 60 % 24)],
        ['lenght comment_1:', len(nearest_comments[0][0])],
        ['lenght comment_2:', len(nearest_comments[0][1])]
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

def nonanalys_data(main_dict, count_analyzed_review = 0):
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

    count_unanalyzed_3 = len(main_dict) - count_analyzed_review
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
    file_name = 'general-stats.cvs'
    save_file(file_name, [[value[0], value[1]] for value in avg_rating(main_dict)])
    save_file(file_name, best_comment(main_dict), 'a')
    save_file(file_name, nearest_reviews(main_dict), 'a')
    save_file(file_name, bad_comment(main_dict), 'a')
    save_file(file_name, nonanalys_data(main_dict, count_analyzed_review), 'a')