from os.path import dirname, abspath, split, join
import csv
from pathlib import Path


def save_file(path, name, data, mode='w'):
    '''function creates a file from the transferred data'''

    Path(join(path, 'resulting data')).mkdir(parents=True, exist_ok=True)
    with open(join(path, 'resulting data', name), mode, newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for line in data:
            writer.writerow(line)
        writer.writerow('')
