import os
from source import get_data
import csv
from operator import itemgetter
from document_creation import file_create


def avg_rating(main_dict):
    '''function returns an average rating (overall) of each application (asin)

    1.1. Task_1.py: to create file general-stats.cvs containing information about
    average rating (overall) of each application (asin);
    '''
    asins_value = {}
    for item in main_dict.values():
        overall, count = asins_value.get(item['asin'], [0, 0])
        asins_value[item['asin']] = [overall + item['overall'], count + 1]
    avg_overall = []
    for key, value in asins_value.items():
        avg_overall.append([key, asins_value.get(key)[0] / asins_value.get(key)[1]])
    return avg_overall

def best_comment(main_dict):
    '''function returns the messages with the most “likes” and the application (asin) associated with it

    1.2. Task_1.py: to create file general-stats.cvs containing information about
    messages with the most “likes” from the entire data set and the application (asin) associated with it;
    '''
    likes = {}
    for key, value in main_dict.items():
        likes[key] = value['helpful'][0]
    sort_likes = sorted(likes.items(), key=itemgetter(1), reverse=True)
    comment = [
        ['messages with the most “likes” from the entire data set and the application (asin) associated with it:'],
        ['like:', main_dict[sort_likes[0][0]]['helpful'][0]],
        ['asin:', main_dict[sort_likes[0][0]]['asin']],
        ['reviewText:', main_dict[sort_likes[0][0]]['reviewText']]
    ]
    return comment

def nearest_review(main_dict):
    '''function returns the shortest interval between ratings of one user and the length of both messages

    Task_1.py: to create file general-stats.cvs containing information about
    the shortest interval between ratings of one user (among all users) and
    the length of both messages which create this interval;
    '''
    all_timereview = {}
    for key, value in main_dict.items():
        if 'reviewerName' in value.keys() and 'unixReviewTime' in value.keys() and value['reviewerName'] != 'Amazon Customer':
            if all_timereview.get(value['reviewerName']) == None:
                all_timereview[value['reviewerName']] = {}
                all_timereview.get(value['reviewerName']).setdefault(key, value['unixReviewTime'])
            else:
                all_timereview.get(value['reviewerName']).setdefault(key, value['unixReviewTime'])
    deltatime = []
    for item in all_timereview.values():
        if len(item) > 1:
            sort = sorted(item.items(), key=itemgetter(1))
            for i in range(1, len(sort)):
                a = i-1
                deltatime.append([sort[i][0], sort[a][0], sort[i][1] - sort[a][1]])
    time_deltatime = []
    global analyzed_data
    for message in deltatime:
        if message[2] != 0:
            time_deltatime.append(message[2])
            analyzed_data.append(message[0])
            analyzed_data.append(message[1])
    for message in deltatime:
        if message[2] == min(time_deltatime):
            comment = [
                ['the shortest interval between ratings of one user (among all users) and the length of both messages which create this interval:'],
                ['interval = ', str(message[2]//60//60) + 'hour ' + str(message[2]//60%60) + 'min '+ str(message[2]%60%60) + 'sec;'],
                ['lenght comment_1:', len(main_dict[message[0]]['reviewText'])],
                ['lenght comment_2:', len(main_dict[message[1]]['reviewText'])]
            ]
            if comment:
                break
    return comment

def bad_comment(main_dict):
    '''function returns the application which received the most useless message

    1.3. Task_1.py: to create file general-stats.cvs containing information about
    the application which received the most useless message;
    '''
    helpfulness = []
    for key, value in main_dict.items():
        if value['helpful'][1] != 0:
            helpfulness.append([key, value['helpful'][0]/value['helpful'][1]])
    result_helpfulness = []
    for message in helpfulness:
        result_helpfulness.append(message[1])
    for message in helpfulness:
        if message[1] == min(result_helpfulness):
            comment = [
                ['the application which received the most useless message:'],
                ['asin:', main_dict[message[0]]['asin']],
                ['reviewText:', main_dict[message[0]]['reviewText']],
                [' helpfulness:', str(message[1])]
            ]
            if comment:
                break
    return comment

def nonanalys_data(main_dict, analyzed_data):
    '''function returns the number of records that cannot be processed for every point above.

    1.5. Task_1.py: to create file general-stats.cvs containing information about
    the number of records that cannot be processed for every point above.
    '''
    comment = ['The number of records that cannot be processed: ']
    count_unanalyzed_1 = 0
    for item in main_dict.values():
        if not 'asin' in item.keys() or not 'overall' in item.keys():
            count_unanalyzed_1 += 1
    comment_1 = [count_unanalyzed_1, ' - for average rating (overall) of each application (asin)']
    comment.append(comment_1)

    count_unanalyzed_2 = 0
    for item in main_dict.values():
        if not 'asin' in item.keys() or not 'helpful' in item.keys() or not 'reviewText' in item.keys():
            count_unanalyzed_2 += 1
    comment_2 = [count_unanalyzed_2, ' - to get the application which received the most useless message']
    comment.append(comment_2)

    count_unanalyzed_3 = len(main_dict) - len(set(analyzed_data))
    comment_3 = [
        str(count_unanalyzed_3) + ' or ' + str(round(count_unanalyzed_3/len(main_dict) * 100)) + '% ',
        ' - to get the shortest interval between ratings of one user (among all users) '
        'and the length of both messages which create this interval;']
    comment.append(comment_3)

    count_unanalyzed_4 = count_unanalyzed_2
    for item in main_dict.values():
        if item['helpful'][1] == 0:
            count_unanalyzed_4 += 1
    comment_4 = [
        str(count_unanalyzed_4) + ' or ' + str(round(count_unanalyzed_4/len(main_dict) * 100)) + '% ',
        ' - to get the application which received the most useless message']
    comment.append(comment_4)
    return comment


if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    analyzed_data = []
    print(avg_rating(main_dict))
    print(len(avg_rating(main_dict)))
    # file_name = 'general-stats.cvs'
    # file_create().save_file(file_name, avg_rating(main_dict))
    # file_create().save_file(file_name, best_comment(main_dict), 'a')
    # file_create().save_file(file_name, nearest_review(main_dict), 'a')
    # file_create().save_file(file_name, bad_comment(main_dict), 'a')
    # file_create().save_file(file_name, nonanalys_data(main_dict, analyzed_data), 'a')




