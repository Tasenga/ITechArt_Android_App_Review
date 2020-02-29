from itertools import groupby
from common_functions import run_func_parallel


class ReviewTimeInfo:
    def __init__(self, time, text):
        self.time = time
        self.text = text


def prepare_data(data):
    return {
        RewiverID: sorted(
            [
                ReviewTimeInfo(group["unixReviewTime"], group["reviewText"])
                for group in groups
            ],
            key=lambda review: review.time,
        )
        for RewiverID, groups in groupby(
            sorted(data, key=lambda review: review["reviewerID"]),
            key=lambda review: review["reviewerID"],
        )
    }


def count_deltatime(data):
    deltatime = []
    for el1, el2 in zip(data[:-1], data[1:]):
        if el2.time >= el1.time:
            deltatime.append([el2.time - el1.time, el2.text, el1.text])
        else:
            raise Exception(f'deltatime should be positive integer. Deltatime '
                            f'was: {el2.time - el1.time}. Please, check data preparation')
    return min(deltatime)


def get_unix_diff_per_name(data):
    return [
        [reviews[0], count_deltatime(reviews[1])]
        if len(reviews[1]) > 1
        else [reviews[0], ["single_review", "single_review", "single_review"]]
        for reviews in data.items()
    ]


def get_potential_bots(data=None):
    if data is None:
        data = []
    return set(map(lambda comment: comment[0] if comment[1][0] == 0 else None, data))


def filter_bot_review(prepared_data, potential_bots):

    analyzed_data = {
        reviewerID: reviews
        for reviewerID, reviews in prepared_data.items()
        if reviewerID not in potential_bots
    }

    number_of_bot_comments = sum(
        [
            len(reviews)
            for reviewerID, reviews in prepared_data.items()
            if reviewerID in potential_bots
        ]
    )
    return analyzed_data, number_of_bot_comments


def process_data(prepared_data):
    unix_diff_per_name = get_unix_diff_per_name(prepared_data)
    potential_bots = get_potential_bots(unix_diff_per_name)
    analyzed_data, number_of_bot_comments = filter_bot_review(prepared_data, potential_bots)
    return analyzed_data, potential_bots, number_of_bot_comments


def analyze_bots_comments(data):
    all_potential_bots = set()
    all_number_of_bot_comments = 0
    all_analyzed_data = {}
    for (analyzed_data, potential_bots, number_of_bot_comments) in run_func_parallel(process_data, run_func_parallel(prepare_data, data)):
        all_potential_bots.update(potential_bots)
        all_number_of_bot_comments += number_of_bot_comments
        for reviewer, reviews in analyzed_data.items():
            all_analyzed_data.setdefault(reviewer, []).extend(reviews)

    # analize_bots_comments_in_concatenated_data
    checked_concatenated_data_for_known_bots, additional_number_of_bot_comments_1 = filter_bot_review(
        all_analyzed_data, all_potential_bots
    )
    all_number_of_bot_comments += additional_number_of_bot_comments_1
    sorted_all_analyzed_data_by_unix = {
        reviewer: sorted(reviews, key=lambda review: review.time)
        for reviewer, reviews in all_analyzed_data.items()
    }
    data_without_bot_comments, new_potential_bots, additional_number_of_bot_comments_2 = process_data(
        sorted_all_analyzed_data_by_unix
    )

    all_number_of_bot_comments += additional_number_of_bot_comments_2

    return data_without_bot_comments, all_number_of_bot_comments


def get_nearest_reviews(data):
    data_without_bot_comments, all_number_of_bot_comments = analyze_bots_comments(data)
    unix_diff_per_name = get_unix_diff_per_name(data_without_bot_comments)
    nearest_reviews = min(
        (review for review in unix_diff_per_name if review[1][1] != "single_review"),
        key=lambda review: review[1][0],
        default=["", [0, "", ""]]
    )
    return nearest_reviews, all_number_of_bot_comments
