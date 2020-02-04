from source import get_data
from operator import itemgetter
from document_creation import file_create


def avg_rating(main_dict, voters=False):
    '''function returns an average rating (overall) of each application (asin)

    1.1. Task_1.py: to create file general-stats.cvs containing information about
    average rating (overall) of each application (asin);
    '''
    asins_value = {}
    for item in main_dict.values():
        overall, count = asins_value.get(item['asin'], [0, 0])
        asins_value[item['asin']] = [overall + item['overall'], count + 1]
    if not voters:
        avg_overall = [[key, str(round(value[0] / value[1], 2)).replace('.', ',')]
                       for key, value in asins_value.items()]
    else:
        avg_overall = [[key, str(round(value[0] / value[1], 2)).replace('.', ','), value[1]]
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
                ['The shortest interval between ratings of one user (among all users) and the length of both messages which create this interval:'],
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
    bad_comment = min(
        dict(filter(lambda review: review[1]['helpful'][1] != 0, main_dict.items())).values(),
        key=lambda review: review['helpful'][0]/review['helpful'][1]
    )
    comment = [
        ['The application which received the most useless message:'],
        ['helpfulness:', str(bad_comment['helpful'][0]/bad_comment['helpful'][1]*100) + '%'],
        ['asin:', bad_comment['asin']],
        ['reviewText:', bad_comment['reviewText']]
    ]
    return comment

def nonanalys_data(main_dict, analyzed_data):
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

    count_unanalyzed_3 = len(main_dict) - len(set(analyzed_data))
    comment.append([str(count_unanalyzed_3) + ' or ' + str(round(count_unanalyzed_3/len(main_dict) * 100)) + '% ',
                    ' - to get the shortest interval between ratings of one user (among all users) '
                    'and the length of both messages which create this interval;'])

    count_unanalyzed_4 = count_unanalyzed_2
    for item in main_dict.values():
        if item['helpful'][1] == 0:
            count_unanalyzed_4 += 1
    comment.append([str(count_unanalyzed_4) + ' or ' + str(round(count_unanalyzed_4/len(main_dict) * 100)) + '% ',
                    ' - to get the application which received the most useless message'])
    return comment


if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    analyzed_data = []
    file_name = 'general-stats.cvs'
    file_create().save_file(file_name, avg_rating(main_dict))
    file_create().save_file(file_name, best_comment(main_dict), 'a')
    file_create().save_file(file_name, nearest_review(main_dict), 'a')
    file_create().save_file(file_name, bad_comment(main_dict), 'a')
    file_create().save_file(file_name, nonanalys_data(main_dict, analyzed_data), 'a')




