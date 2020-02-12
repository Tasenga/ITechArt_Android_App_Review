from os.path import dirname, abspath, split, join
import csv
from pathlib import Path
from json import loads, dump

project_path, folder = split(dirname(abspath(__file__)))

def get_data_from_json(modulename, filename, path=project_path):
    """function returns a list of dictionaries from the json datafile"""
    in_dir = Path(join(path, modulename, "source"))
    with Path(in_dir, filename).open() as file:
        return tuple(loads(row) for row in file)

def get_data_from_csv(modulename, filename, path=project_path):
    """function returns a list of dictionaries from the csv datafile"""
    in_dir = Path(join(path, modulename, "source"))
    with Path(in_dir, filename).open() as file:
        return tuple(row for row in file)

def save_file(modulename, filename, data, mode="w", path=project_path):
    """function creates a file from the transferred data"""
    out_dir = Path(join(path, modulename, "resulting data"))
    out_dir.mkdir(parents=True, exist_ok=True)
    with Path(out_dir, filename).open(mode=mode, newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        for line in data:
            writer.writerow(line)
        writer.writerow("")

def get_separeted_data_from_json(modulename, filename, path=project_path):
    """function returns dictionaries from the json datafile"""
    in_dir = Path(join(path, modulename, "source"))
    with Path(in_dir, filename).open() as file:
        start = 0
        end = 752973
        data1 = []
        data2 = []
        for row in file:
            if start in range(0, end // 4):
                data1.append(loads(row))
            else:
                data2.append(loads(row))
            start += 1
    return data1, data2

def create_source_data_from_json(data, modulename, filename, path=project_path):
    """function creates a json file from the json object"""
    out_dir = Path(join(path, modulename, "source"))
    with Path(out_dir, filename).open(mode="w") as file:
        for row in data:
            dump(row, file)
            file.write("\n")

if __name__ == "__main__":
    data1, data2 = get_separeted_data_from_json(
        "FP_analysis_of_reviews_from_Amazon", "Apps_for_Android_5.json"
    )
    create_source_data_from_json(
        data1, "FP_analysis_of_reviews_from_Amazon", "part1_Apps_for_Android_5.json"
    )
    create_source_data_from_json(
        data2, "FP_analysis_of_reviews_from_Amazon", "part2_Apps_for_Android_5.json"
    )
