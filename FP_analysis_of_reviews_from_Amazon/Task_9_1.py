from pathlib import Path
from os.path import dirname, abspath
from common_module.work_with_document import get_data_from_json, save_file
from concurrent.futures import ProcessPoolExecutor
from common_functions import *
from nearest_review import main


def best_comment(data):
    """function returns the messages with the most “likes” and the application (asin) associated with it

    1.2. Task_9_1.py: to create file general-stats.cvs containing information about
    messages with the most “likes” from the entire data set and the application (asin) associated with it;
    """
    return max(data, key=lambda review: review["helpful"][0])

def bad_comment(data):
    """function returns the application which received the most useless message

    1.3. Task_9_1: to create file general-stats.cvs containing information about
    the application which received the most useless message;
    """
    return min(
        list(filter(lambda review: review["helpful"][1] != 0, data)),
        key=lambda review: review["helpful"][0] / review["helpful"][1],
    )


def nonanalys_data(reviews):
    """function returns the number of records that cannot be processed for every point above.

    1.5. Task_9_1: to create file general-stats.cvs containing information about
    the number of records that cannot be processed for every point above.
    """
    def count_unanalyzed(*required_keys):
        return len(
            [review for review in reviews
             if [all([key not in review for key in required_keys])]]
        )

    return (
        count_unanalyzed("asin", "overall"),  # avg score
        count_unanalyzed("asin", "helpful", "reviewText"),  # best comment,
        len(list(filter(lambda it: it["helpful"][1] == 0, reviews))),  # bad comment
    )


if __name__ == "__main__":

    chunks = Path(dirname(abspath(__file__)), "source", "data").iterdir()
    data = run_func_parallel(get_data_from_json, chunks)
    filename = "general-stats.cvs"

    apps_scores = {}
    for result in run_func_parallel(get_apps_scores, data):
        apps_scores = get_dict_of_apps_with_score(result, apps_scores)

    save_file(
        Path(dirname(abspath(__file__))),
        filename,
        tuple(
            map(
                lambda app: (app.asin, app.average_score, app.number_of_votes),
                apps_scores.values(),
            )
        ),
    )


    best_review = best_comment(run_func_parallel(best_comment, data))
    comment_for_best_review = [
        ["Messages with the most “likes” from the entire data set and the application (asin) associated with it:"],
        ["like:", best_review["helpful"][0]],
        ["asin:", best_review["asin"]],
        ["reviewText:", best_review["reviewText"]],
    ]
    save_file(Path(dirname(abspath(__file__))), filename, comment_for_best_review, "a")


    nearest_comments, all_number_of_bot_comments = main(data)
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
        ["length comment_1:", len(nearest_comments[1][1])],
        ["length comment_2:", len(nearest_comments[1][2])],
    ]
    save_file(Path(dirname(abspath(__file__))), filename, comment_for_nearest_review, "a")

    bad_review = bad_comment(run_func_parallel(bad_comment, data))
    comment_for_bad_review = [
        ["The application which received the most useless message:"],
        [
            "helpfulness:",
            "{}%".format(bad_review["helpful"][0] / bad_review["helpful"][1] * 100),
        ],
        ["asin:", bad_review["asin"]],
        ["reviewText:", bad_review["reviewText"]],
    ]
    save_file(Path(dirname(abspath(__file__))), filename, comment_for_bad_review, "a")

    with ProcessPoolExecutor() as executor:
        common_count_unanalyzed_avg_score = 0
        common_count_unanalyzed_best_comment = 0
        common_count_unanalyzed_bad_comment = 0
        for (
            count_unanalyzed_avg_score,
            count_unanalyzed_best_comment,
            count_unanalyzed_bad_comment,
        ) in executor.map(nonanalys_data, data):
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
                round(all_number_of_bot_comments / (sum(map(lambda it: len(it), data))) * 100),
            ),
            " - to get the shortest interval between ratings of one user (among all users) "
            "and the length of both messages which create this interval;",
        ],
        [
            "{} or {}%".format(
                common_count_unanalyzed_bad_comment,
                round(
                    common_count_unanalyzed_bad_comment
                    / (sum(map(lambda it: len(it), data)))
                    * 100
                ),
            ),
            " - to get the application which received the most useless message",
        ],
    ]
    save_file(Path(dirname(abspath(__file__))), filename, comment_for_count_unanalyzed_data, "a")
