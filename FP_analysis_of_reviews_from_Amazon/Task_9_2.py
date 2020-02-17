from common_module.work_with_document import get_data_from_json, save_file
from common_functions import get_dict_of_apps_with_score, get_apps_scores, run_func_parallel, AppScore
from pathlib import Path
from os.path import dirname, abspath, join


if __name__ == "__main__":

    chunks = Path(dirname(abspath(__file__)), "source", "data").iterdir()
    data = run_func_parallel(get_data_from_json, chunks)

    # path_to_save
    Path(dirname(abspath(__file__)), "resulting data").mkdir(parents=True, exist_ok=True)
    path_to_save = Path(dirname(abspath(__file__)), "resulting data", "apps-stats.cvs")

    apps_scores = get_dict_of_apps_with_score(data)

    save_file(
        path_to_save,
        [(app.asin, app.average_score, app.number_of_votes) for app in apps_scores.values()]
    )