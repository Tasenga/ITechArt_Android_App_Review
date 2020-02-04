import json
import os
import gzip

def open_gzip(archivename = 'reviews_Apps_for_Android_5.json.gz'):
    '''functions return dictionary from the datafile'''

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with gzip.open(os.path.join(ROOT_DIR, archivename), 'rb') as gzip_file:
            my_dict = {}
            i = 1
            for row in gzip_file:
                my_dict[i] = json.loads(row)
                i += 1
    return my_dict