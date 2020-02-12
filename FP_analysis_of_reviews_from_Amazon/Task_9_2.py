from common_module.work_with_document import get_data_from_json, save_file
from common_functions import get_apps_scores_parallel, AppScore


if __name__ == "__main__":

    modulename = "FP_analysis_of_reviews_from_Amazon"
    data1 = get_data_from_json(modulename, "part1_Apps_for_Android_5.json")
    data2 = get_data_from_json(modulename, "part2_Apps_for_Android_5.json")

    apps_scores = get_apps_scores_parallel(data1, data2)

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