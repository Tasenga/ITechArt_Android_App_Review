import os
from source import get_data
import csv


def avg_rating(main_dict):
    '''function returns average rating of each application and number of voters

    2.1. Task_2.py: to create file apps-stats.cvs containing information about
    average rating (overall) of each application (asin) and number of voters.
    '''
    asins = []
    for item in main_dict.values():
        asins.append(item['asin'])
    asins_value = dict.fromkeys(set(asins), [0, 0])
    for item in main_dict.values():
        asins_value[item['asin']] = [asins_value.get(item['asin'])[0] + item['overall'], asins_value.get(item['asin'])[1]+1]
    avg_overall = []
    for key, value in asins_value.items():
        avg_overall.append([key, asins_value.get(key)[0] / asins_value.get(key)[1], asins_value.get(key)[1]])
    return avg_overall

# create file apps-stats.cvs containing information above:
def file_create(data):
    path = os.path.dirname(os.path.abspath(__file__))
    try:
        os.mkdir(os.path.join(path, 'resulting data'))
    except:
        pass
    with open(os.path.join(path, 'resulting data', 'apps-stats.cvs'), "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for line in data:
            writer.writerow(line)

if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    file_create(avg_rating(main_dict))