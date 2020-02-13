from common_module.work_with_document import get_data_from_json, save_file
from common_functions import get_apps_scores_parallel, AppScore
from os import walk
from os.path import dirname, abspath, join
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":

    documents = []
    for root, dir, files in walk(join(dirname(abspath(__file__)), "source", "data")):
        for name in files:
            documents.append(join(root, name))

    data = []
    with ProcessPoolExecutor() as executor:
        for part_of_data in executor.map(get_data_from_json, documents):
            data.extend(part_of_data)

    apps_scores = get_apps_scores_parallel(data)

    modulename = "FP_analysis_of_reviews_from_Amazon"
    save_file(
        modulename,
        "apps-stats.cvs",
        tuple(
            map(
                lambda app: (app.asin, app.average_score, app.number_of_votes),
                apps_scores.values(),
            )
        ),
    )


    # ANOTHER WAY (13.5sec)
    # from common_functions import concatenate_apps_scores
    # save_file(
    #     modulename,
    #     "apps-stats.cvs",
    #     tuple(
    #         map(
    #             lambda app: (app.asin, app.average_score, app.number_of_votes),
    #             concatenate_apps_scores(apps_scores),
    #         )
    #     ),
    # )