
def avg_rating(main_dict):
    '''function returns an average rating (overall) of each application (asin)

    1.1. Task_1.py: to create file general-stats.cvs containing information about
    average rating (overall) of each application (asin);
    2.1. Task_2.py: to create file apps-stats.cvs containing information about
    average rating (overall) of each application (asin) and number of voters.
    '''

    asins_value = {}
    for item in main_dict:
        overall, count = asins_value.get(item['asin'], [0, 0])
        asins_value[item['asin']] = [overall + item['overall'], count + 1]
    avg_overall = [[key, '{}'.format(round(value[0] / value[1], 2)), value[1]]
                   for key, value in asins_value.items()]
    return avg_overall