import os
import csv
from collections import Counter
from itertools import groupby
from operator import itemgetter


def get_data(filename):
    '''function return a dictionary from the datafile'''

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(ROOT_DIR, filename)) as file:
        reader = csv.reader(file)
        main_dict = [{'ITEM_ID': row[0], 'STORE_ID': row[1], 'PRICE': row[2], 'APPROVED_BY': row[3]} for row in reader]
    return main_dict

def count_unique_values(main_dict, field):
    '''function return a number of unique values for a field which was given like function's parameter'''
    result = len(set([item[field] for item in main_dict]))
    # result = len([key for key, item in groupby(main_dict, key=lambda position: position[field])])
    return result

def get_user_by_approves(main_dict):
    '''function return a user name who approved the highest number of prices'''
    result = [i for key, value in groupby(sorted(main_dict, key=lambda position: position['APPROVED_BY']), key=lambda position: position['APPROVED_BY']) for i in value]
    return result

#                 - the user who approved the highest number of prices;
#                 - the number of products sold in each store;
#                 - the average cost of each product;
#                 - shops which selling the most expensive and cheapest product (indicating the product and its price).


if __name__ == "__main__":
    main_dict = get_data('prices.csv')
    count_unique_values(main_dict, 'STORE_ID')
    get_user_by_approves(main_dict)
    print(get_user_by_approves(main_dict))
