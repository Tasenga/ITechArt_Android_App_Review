import json
import os


def get_data(filename):
    '''function returns two lists of dictionaries from the datafile'''

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(ROOT_DIR, filename)) as file:
        start = 1
        end = 0
        for row in file:
            end += 1

    with open(os.path.join(ROOT_DIR, filename)) as file:
        data1 = []
        data2 = []
        for row in file:
            if start in range(1, end // 2):
                data1.append(json.loads(row))
            if start in range(end // 2, end + 1):
                data2.append(json.loads(row))
            start += 1

    return data1, data2