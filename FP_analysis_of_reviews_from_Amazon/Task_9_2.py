from common_module.work_with_document import get_data_from_json, save_file
from common_functions import get_apps_scores_concurrent_future, AppScore


if __name__ == "__main__":

    modulename = "FP_analysis_of_reviews_from_Amazon"
    data1 = get_data_from_json(modulename, "part1_Apps_for_Android_5.json")
    data2 = get_data_from_json(modulename, "part2_Apps_for_Android_5.json")
    data3 = get_data_from_json(modulename, "part3_Apps_for_Android_5.json")
    data4 = get_data_from_json(modulename, "part4_Apps_for_Android_5.json")

    apps_scores = get_apps_scores_concurrent_future(data1, data2, data3, data4)

    save_file(
        modulename,
        "apps-stats.cvs",
        [
            [app.asin, app.average_score, app.number_of_votes]
            for app in apps_scores.values()
        ],
    )
