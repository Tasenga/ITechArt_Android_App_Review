import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_data():
    '''function return a dictionary from the datafile'''
    with open(os.path.join(ROOT_DIR, 'source', 'Apps_for_Android_5.json')) as file:
        start = 1
        end = 0
        for row in file:
            end += 1
        print(end)

    with open(os.path.join(ROOT_DIR, 'source', 'Apps_for_Android_5.json')) as file:
        data1 = []
        data2 = []
        for row in file:
            if start in range(1, end // 2):
                data1.append(json.loads(row))
            if start in range(end // 2, end + 1):
                data2.append(json.loads(row))
            start += 1
    return data1, data2

def create(data, filename):
    with open(os.path.join(ROOT_DIR, 'source', filename), 'w') as file:
        for row in data:
            file.write(str(row) + '\n')



data1, data2 = get_data()
create(data1, 'data1.json')
create(data2, 'data2.json')

