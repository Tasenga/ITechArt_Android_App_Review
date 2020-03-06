from os.path import dirname, abspath, split, join
import csv
from pathlib import Path
from json import loads, dump

project_path, folder = split(dirname(abspath(__file__)))

def get_data_from_json(file):
    """function returns a list of dictionaries from the json datafile"""
    with Path(file).open() as file:
        return [loads(row) for row in file]

def get_data_from_csv(file):
    """function returns a list of dictionaries from the csv datafile"""
    with Path(file).open() as file:
        return tuple(row for row in file)

def save_file(file, data, mode="w"):
    """function creates a file from the transferred data"""
    with Path(file).open(mode=mode, newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        for line in data:
            writer.writerow(line)
        writer.writerow("")

def get_separeted_data_from_json(path, filename):
    """function returns dictionaries from the json datafile"""
    with Path(path, filename).open() as file:
        start = 0
        end = 752973
        data1 = []
        data2 = []
        for row in file:
            if start in range(0, end // 2):
                data1.append(loads(row))
            else:
                data2.append(loads(row))
            start += 1
    return data1, data2

def create_source_data_from_json(path, filename, data):
    """function creates a json file from the json object"""
    with Path(path, filename).open(mode="w") as file:
        for row in data:
            dump(row, file)
            file.write("\n")

if __name__ == "__main__":
    data1, data2 = get_separeted_data_from_json(
        Path(join(project_path, "FP_analysis_of_reviews_from_Amazon", "source", "archive")),
        "Apps_for_Android_5.json"
    )
    create_source_data_from_json(
        Path(join(project_path, "FP_analysis_of_reviews_from_Amazon", "source", "data")),
        "part1_Apps_for_Android_5.json",
        data1
    )
    create_source_data_from_json(
        Path(join(project_path, "FP_analysis_of_reviews_from_Amazon", "source", "data")),
        "part2_Apps_for_Android_5.json",
        data2
    )
