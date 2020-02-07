import os
import csv
from collections import Counter
from itertools import groupby
from operator import itemgetter


def get_data(filename):
    '''function returns a dictionary from the datafile'''

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(ROOT_DIR, filename)) as file:
        reader = csv.reader(file)
        main_dict = [{'ITEM_ID': row[0], 'STORE_ID': row[1], 'PRICE': row[2], 'APPROVED_BY': row[3]} for row in reader]
        del main_dict[0]
    return main_dict

def count_unique_values(main_dict, field):
    '''function returns the number of unique values for a field which was given like function's parameter'''

    result = len(set([item[field] for item in main_dict]))
    return result

def get_user_by_approves(main_dict):
    '''function returns the user name who approved the highest number of prices'''

    result = max(
        (
            (key, len(list(value)))
            for key, value
            in groupby(sorted(main_dict, key=lambda position: position['APPROVED_BY']),
                       key=lambda position: position['APPROVED_BY'])
        ),
        key=lambda x: x[1]
    )
    return result

def get_products_in_stores(main_dict):
    '''function returns the number of products sold in each store'''

    result = {
        STORE_ID: len(set(position['ITEM_ID'] for position in positions))
        for STORE_ID, positions
        in groupby(
            sorted(main_dict, key=lambda position: position['STORE_ID']),
            key=lambda position: position['STORE_ID'])
    }
    return result

def get_avg_cost_per_products(main_dict):
    '''function returns the average cost of each product'''

    def count_avg(positions):
        '''function returns the average cost of the product'''
        price = 0
        count = 0
        for position in positions:
            price += float(position['PRICE'])
            count += 1
        return round(price / count, 2)

    result = {
        ITEM_ID: count_avg(positions)
        for ITEM_ID, positions
        in groupby(
            sorted(main_dict, key=lambda position: position['ITEM_ID']),
            key=lambda position: position['ITEM_ID'])

    }
    return result

def get_exp_and_chp_product(main_dict):
    '''function returns the shops which selling the most expensive
    and cheapest product (indicating the product and its price).'''

    result = [max(item[''])
        for item
        in main_dict
    ]

    return result





if __name__ == "__main__":
    main_dict = get_data('prices.csv')
    count_unique_values(main_dict, 'STORE_ID')
    count_unique_values(main_dict, 'ITEM_ID')
    print(count_unique_values(main_dict, 'STORE_ID'))
    print(count_unique_values(main_dict, 'ITEM_ID'))
    print(get_user_by_approves(main_dict))
    print(get_products_in_stores(main_dict))
    print(get_avg_cost_per_products(main_dict))
