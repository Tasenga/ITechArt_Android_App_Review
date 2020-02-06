import json
import os


def get_data(filename):
    '''function return a dictionary from the datafile'''

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(ROOT_DIR, filename)) as file:
        main_dict = [json.loads(row) for row in file]
    return main_dict