import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_data():
    '''function return a dictionary from the datafile'''
    with open(os.path.join(ROOT_DIR, 'source', 'Apps_for_Android_5.json')) as file:
        start = 0
        end = 752973
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        for row in file:
            if start in range(0, end // 4):
                data1.append(json.loads(row))
            if start in range(end // 4, end // 2):
                data2.append(json.loads(row))
            if start in range(end // 2, (end - end // 4)):
                data3.append(json.loads(row))
            if start in range((end - end // 4), end + 1):
                data4.append(json.loads(row))
            start += 1
    return data1, data2, data3, data4

def create(data, filename):
    with open(os.path.join(ROOT_DIR, 'source', filename), 'w') as file:
        for row in data:
            json.dump(row, file)
            file.write('\n')


if __name__ == '__main__':
    data1, data2, data3, data4 = get_data()
    create(data1, 'part1_Apps_for_Android_5.json')
    create(data2, 'part2_Apps_for_Android_5.json')
    create(data3, 'part3_Apps_for_Android_5.json')
    create(data4, 'part4_Apps_for_Android_5.json')


