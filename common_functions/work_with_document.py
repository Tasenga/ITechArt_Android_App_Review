from os.path import dirname, abspath, split, join
import csv
from pathlib import Path
from json import loads

project_path, folder = split(dirname(abspath(__file__)))

def get_data_from_json(modulename, filename, path=project_path):
    """function returns a list of dictionaries from the json datafile"""
    in_dir = Path(join(path, modulename, "source"))
    with Path(in_dir, filename).open() as file:
        return [loads(row) for row in file]

def get_data_from_csv(modulename, filename, path=project_path):
    """function returns a list of dictionaries from the csv datafile"""
    in_dir = Path(join(path, modulename, "source"))
    with Path(in_dir, filename).open() as file:
        # reader = csv.reader(file)
        return [row for row in file]

def save_file(modulename, name, data, mode="w", path=project_path):
    """function creates a file from the transferred data"""
    out_dir = Path(join(path, modulename, "resulting data"))
    out_dir.mkdir(parents=True, exist_ok=True)
    with Path(out_dir, name).open(mode=mode, newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        for line in data:
            writer.writerow(line)
        writer.writerow("")
