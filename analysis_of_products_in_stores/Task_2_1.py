import os
import csv
from itertools import groupby
from collections import Counter
from common_functions.work_with_document import save_file

def get_data(filename):
    """function returns a dictionary from the datafile"""

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(ROOT_DIR, filename)) as file:
        reader = csv.reader(file)
        next(reader)
        main_dict = [
            {
                "ITEM_ID": row[0],
                "STORE_ID": row[1],
                "PRICE": float(row[2]),
                "APPROVED_BY": row[3],
            }
            for row in reader
        ]
    return main_dict

def sort_dict(dict, field):
    """function returns a sorted dictionary for a field which was given like function's parameter and this parameter"""

    sorted_dict = sorted(dict, key=lambda position: position[field])
    return sorted_dict, field

def group_dict(def_sort_dict):
    """function returns a grouped dictionary"""

    grouped_dict = {
        key: [group for group in groups]
        for key, groups
        in groupby(def_sort_dict[0], key=lambda position: position[def_sort_dict[1]])
    }
    return grouped_dict

def count_unique_values(dict):
    """function returns the number of unique values for a field which was given like function's parameter"""
    count_unique_values = 0
    for i in dict:
        count_unique_values += 1
    return count_unique_values

def get_user_by_approves(dict):
    """function returns the user name who approved the highest number of prices"""

    result = max(((key, len(dict[key])) for key in dict.keys()), key=lambda x: x[1])
    return result

def get_products_in_stores(dict):
    """function returns the number of products sold in each store"""

    result = {
        STORE_ID: len(set(position["ITEM_ID"] for position in positions))
        for STORE_ID, positions in dict.items()
    }
    return result

def get_avg_cost_per_products(dict):
    """function returns the average cost of each product"""
    def count_avg(positions):
        """function returns the average cost of the product"""
        price = 0
        count = 0
        for position in positions:
            price += position["PRICE"]
            count += 1
        return round(price / count, 2)
    result = {ITEM_ID: count_avg(positions) for ITEM_ID, positions in dict.items()}
    return result

def get_exp_and_chp_products(main_dict):
    """function returns the shops which selling the most expensive
    and cheapest product (indicating the product and its price)."""

    sorted_main_dict, field = sort_dict(main_dict, "PRICE")
    exp_product = [
        sorted_main_dict[-1]["STORE_ID"],
        sorted_main_dict[-1]["ITEM_ID"],
        sorted_main_dict[-1]["PRICE"],
    ]
    chp_product = [
        sorted_main_dict[0]["STORE_ID"],
        sorted_main_dict[0]["ITEM_ID"],
        sorted_main_dict[0]["PRICE"],
    ]
    return exp_product, chp_product

if __name__ == "__main__":
    main_dict = get_data("prices.csv")
    dict_by_ITEM_ID = group_dict(sort_dict(main_dict, "ITEM_ID"))
    dict_by_STORE_ID = group_dict(sort_dict(main_dict, "STORE_ID"))
    dict_by_APPROVED = group_dict(sort_dict(main_dict, "APPROVED_BY"))

    filename = "L8_result.csv"

    uniq_store_comment = ["The number of unique STORE:", [count_unique_values(dict_by_STORE_ID)]]
    save_file(filename, uniq_store_comment)

    uniq_item_comment = ["The number of unique ITEM:", [count_unique_values(dict_by_ITEM_ID)]]
    save_file(filename, uniq_item_comment, "a")

    user_approved = get_user_by_approves(dict_by_APPROVED)
    user_approved_comment = [
        ["The user name who approved the highest number of prices:", user_approved[0]],
        ["The number of approved prices by user:", user_approved[1]],
    ]
    save_file(filename, user_approved_comment, "a")

    save_file(
        filename,
        [[key, value] for key, value in get_products_in_stores(dict_by_STORE_ID).items()],
        "a",
    )

    save_file(
        filename,
        [[key, value] for key, value in get_avg_cost_per_products(dict_by_ITEM_ID).items()],
        "a",
    )

    exp_product, chp_product = get_exp_and_chp_products(main_dict)
    exp_and_chp_products = [
        ["The STORE with the most expensive product:", exp_product[0]],
        ["The most expensive product:", exp_product[1]],
        ["The highest price:", exp_product[2]],
        ["The STORE with the most cheapest product:", chp_product[0]],
        ["The most cheapest product:", chp_product[1]],
        ["The lowest price:", chp_product[2]],
    ]
    save_file(filename, exp_and_chp_products, "a")

    # print(count_unique_values(dict_by_ITEM_ID))
    # print(count_unique_values(dict_by_STORE_ID))
    # print(get_user_by_approves(dict_by_APPROVED))
    # print(get_products_in_stores(dict_by_STORE_ID))
    # print(get_avg_cost_per_products(dict_by_ITEM_ID))
    # print(get_exp_and_chp_products(main_dict))
