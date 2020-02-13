from common_module.work_with_document import get_data_from_json, save_file
from concurrent.futures import ProcessPoolExecutor
from common_functions import get_apps_scores_parallel
from nearest_review import (
    get_processing_data_parallel,
    process_data,
    get_unix_diff_per_name,
    get_nearest_review,
)
from time import time

def best_comment(data):
    """function returns the messages with the most “likes” and the application (asin) associated with it

    1.2. Task_9_1.py: to create file general-stats.cvs containing information about
    messages with the most “likes” from the entire data set and the application (asin) associated with it;
    """
    best_comment = max(data, key=lambda review: review["helpful"][0])
    return best_comment

def bad_comment(data):
    """function returns the application which received the most useless message

    1.3. Task_9_1: to create file general-stats.cvs containing information about
    the application which received the most useless message;
    """
    bad_comment = min(
        list(filter(lambda review: review["helpful"][1] != 0, data)),
        key=lambda review: review["helpful"][0] / review["helpful"][1],
    )
    return bad_comment

def nonanalys_data(data):
    """function returns the number of records that cannot be processed for every point above.

    1.5. Task_9_1: to create file general-stats.cvs containing information about
    the number of records that cannot be processed for every point above.
    """
    count_unanalyzed_avg_score = len(
        dict(
            filter(
                lambda review: "asin" not in review.keys()
                or "overall" not in review.keys(),
                data,
            )
        )
    )

    count_unanalyzed_best_comment = len(
        dict(
            filter(
                lambda review: "asin" not in review.keys()
                or "helpful" not in review.keys()
                or "reviewText" not in review.keys(),
                data,
            )
        )
    )

    count_unanalyzed_bad_comment = len(
        dict(filter(lambda review: review[0]["helpful"][1] == 0, data))
    )
    return (
        count_unanalyzed_avg_score,
        count_unanalyzed_best_comment,
        count_unanalyzed_bad_comment,
    )

if __name__ == "__main__":
    modulename = "FP_analysis_of_reviews_from_Amazon"
    data1 = get_data_from_json(modulename, "part1_Apps_for_Android_5.json")
    data2 = get_data_from_json(modulename, "part2_Apps_for_Android_5.json")
    filename = "general-stats.cvs"

    apps_scores = get_apps_scores_parallel(data1, data2)
    save_file(
        modulename,
        filename,
        tuple(map(lambda app: (app.asin, app.average_score), apps_scores.values())),
    )

    with ProcessPoolExecutor() as executor:
        best_review = best_comment(tuple(executor.map(best_comment, (data1, data2))))
    comment_for_best_review = [
        ["Messages with the most “likes” from the entire data set and the application (asin) associated with it:"],
        ["like:", best_review["helpful"][0]],
        ["asin:", best_review["asin"]],
        ["reviewText:", best_review["reviewText"]],
    ]
    save_file(modulename, filename, comment_for_best_review, "a")

    sorted_processing_data, all_number_of_bot_comments = get_processing_data_parallel(
        data1, data2
    )
    analyzed_data, potential_bots, number_of_bot_comments = process_data(
        sorted_processing_data
    )
    all_number_of_bot_comments += number_of_bot_comments
    unix_diff_per_name = get_unix_diff_per_name(analyzed_data)
    nearest_comments = get_nearest_review(unix_diff_per_name)
    comment_for_nearest_review = [
        [
            "The shortest interval between ratings of one user (among all users) "
            "and the length of both messages which create this interval:"
        ],
        [
            "interval = ",
            "{} days {} hour {} min {} sec;".format(
                nearest_comments[1][0] // 60 // 60 // 24,
                nearest_comments[1][0] // 60 // 60 % 24,
                nearest_comments[1][0] // 60 % 60 % 24,
                nearest_comments[1][0] % 60 % 60 % 24,
            ),
        ],
        ["lenght comment_1:", len(nearest_comments[1][1])],
        ["lenght comment_2:", len(nearest_comments[1][2])],
    ]
    save_file(modulename, filename, comment_for_nearest_review, "a")

    with ProcessPoolExecutor() as executor:
        bad_review = bad_comment(tuple(executor.map(bad_comment, (data1, data2))))
    comment_for_bad_review = [
        ["The application which received the most useless message:"],
        [
            "helpfulness:",
            "{}%".format(bad_review["helpful"][0] / bad_review["helpful"][1] * 100),
        ],
        ["asin:", bad_review["asin"]],
        ["reviewText:", bad_review["reviewText"]],
    ]
    save_file(modulename, filename, comment_for_bad_review, "a")

    with ProcessPoolExecutor() as executor:
        common_count_unanalyzed_avg_score = 0
        common_count_unanalyzed_best_comment = 0
        common_count_unanalyzed_bad_comment = 0
        for (
            count_unanalyzed_avg_score,
            count_unanalyzed_best_comment,
            count_unanalyzed_bad_comment,
        ) in executor.map(nonanalys_data, (data1, data2)):
            common_count_unanalyzed_avg_score += count_unanalyzed_avg_score
            common_count_unanalyzed_best_comment += count_unanalyzed_best_comment
            common_count_unanalyzed_bad_comment += count_unanalyzed_bad_comment

    comment_for_count_unanalyzed_data = [
        ["The number of records that cannot be processed: "],
        [
            common_count_unanalyzed_avg_score,
            " - for average rating (overall) of each application (asin)",
        ],
        [
            common_count_unanalyzed_best_comment,
            " - to get the application which received the most useless message",
        ],
        [
            "{} or {}%".format(
                all_number_of_bot_comments,
                round(all_number_of_bot_comments / (len(data1) + len(data2)) * 100),
            ),
            " - to get the shortest interval between ratings of one user (among all users) "
            "and the length of both messages which create this interval;",
        ],
        [
            "{} or {}%".format(
                common_count_unanalyzed_bad_comment,
                round(
                    common_count_unanalyzed_bad_comment
                    / (len(data1) + len(data2))
                    * 100
                ),
            ),
            " - to get the application which received the most useless message",
        ],
    ]
    save_file(modulename, filename, comment_for_count_unanalyzed_data, "a")
