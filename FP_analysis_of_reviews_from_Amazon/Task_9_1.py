from pathlib import Path
from os.path import dirname, abspath
from common_module.work_with_document import get_data_from_json, save_file
from common_functions import *
from nearest_review import get_nearest_reviews


def best_comment(data):
    """function returns the messages with the most “likes” and the application (asin) associated with it

    1.2. Task_9_1.py: to create file general-stats.cvs containing information about
    messages with the most “likes” from the entire data set and the application (asin) associated with it;
    """
    return max(data, key=lambda review: review["helpful"][0],
               default={"asin": None, "helpful": [None, None], "reviewText": None})

def bad_comment(data):
    """function returns the application which received the most useless message

    1.3. Task_9_1: to create file general-stats.cvs containing information about
    the application which received the most useless message;
    """
    return min([review for review in data if review["helpful"][1] != 0],
               key=lambda review: review["helpful"][0] / review["helpful"][1],
               default={"asin": None, "helpful": [float('inf'), 1], "reviewText": None})


def nonanalys_data(data):
    """function returns the number of records that cannot be processed for every point above.

    1.5. Task_9_1: to create file general-stats.cvs containing information about
    the number of records that cannot be processed for every point above.
    """
    def count_unanalyzed(*required_keys):
        return len(
            [review for review in data
             if any(key not in review.keys() for key in required_keys)]
        )

    return (
        count_unanalyzed("asin", "overall"),  # avg score
        count_unanalyzed("asin", "reviewText"),  # best comment,
        len([review for review in data if review["helpful"][1] == 0]),  # bad comment
    )

def total_nonanalys_data(data):
    common_count_unanalyzed_avg_score = 0
    common_count_unanalyzed_best_comment = 0
    common_count_unanalyzed_bad_comment = 0
    for (count_unanalyzed_avg_score,
         count_unanalyzed_best_comment,
         count_unanalyzed_bad_comment) in run_func_parallel(nonanalys_data, data):
        common_count_unanalyzed_avg_score += count_unanalyzed_avg_score
        common_count_unanalyzed_best_comment += count_unanalyzed_best_comment
        common_count_unanalyzed_bad_comment += count_unanalyzed_bad_comment
    return (common_count_unanalyzed_avg_score,
            common_count_unanalyzed_best_comment, 
            common_count_unanalyzed_bad_comment)


if __name__ == "__main__":

    cwd = dirname(abspath(__file__))
    chunks = Path(cwd, "source", "data").iterdir()
    data = run_func_parallel(get_data_from_json, chunks)

    # path_to_save
    path = Path(cwd, "resulting data")
    path.mkdir(parents=True, exist_ok=True)
    file_to_save = Path(path, "general-stats.cvs")

    apps_scores = get_dict_of_apps_with_score(data)
    save_file(
        file_to_save,
        [(app.asin, app.average_score) for app in apps_scores.values()],
    )


    best_review = best_comment(run_func_parallel(best_comment, data))
    comment_for_best_review = [
        ["Messages with the most “likes” from the entire data set and the application (asin) associated with it:"],
        ["like:", best_review["helpful"][0]],
        ["asin:", best_review["asin"]],
        ["reviewText:", best_review["reviewText"]],
    ]
    save_file(file_to_save, comment_for_best_review, "a")


    nearest_comments, all_number_of_bot_comments = get_nearest_reviews(data)
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
    save_file(file_to_save, comment_for_nearest_review, "a")


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
    save_file(file_to_save, comment_for_bad_review, "a")


    (common_count_unanalyzed_avg_score,
     common_count_unanalyzed_best_comment,
     common_count_unanalyzed_bad_comment) = total_nonanalys_data(data)
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
    save_file(file_to_save, comment_for_count_unanalyzed_data, "a")
