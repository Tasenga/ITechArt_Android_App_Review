import os
import csv


def create_directory():
    '''function creates a directory to save files'''
    try:
        os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resulting data'))
    except:
        pass
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resulting data')
    return path

def save_file(name, data, mode='w'):
    '''function creates a file from the transferred data'''
    with open(os.path.join(create_directory(), name), mode, newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for line in data:
            writer.writerow(line)
        writer.writerow('')