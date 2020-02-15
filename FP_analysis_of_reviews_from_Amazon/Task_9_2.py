from common_module.work_with_document import get_data_from_json, save_file
from common_functions import get_dict_of_apps_with_score, get_apps_scores, run_func_parallel, AppScore
from pathlib import Path
from os.path import dirname, abspath
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":

    chunks = Path(dirname(abspath(__file__)), "source", "data").iterdir()
    data = run_func_parallel(get_data_from_json, chunks)

    apps_scores = {}
    for result in run_func_parallel(get_apps_scores, data):
        apps_scores = get_dict_of_apps_with_score(result, apps_scores)

    save_file(
        Path(dirname(abspath(__file__))),
        "apps-stats.cvs",
        tuple(
            map(
                lambda app: (app.asin, app.average_score, app.number_of_votes),
                apps_scores.values(),
            )
        ),
    )