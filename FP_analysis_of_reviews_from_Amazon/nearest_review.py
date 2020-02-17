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
    return min(
        (data[i].time - data[i - 1].time, data[i].text, data[i - 1].text)
        for i in range(1, len(data))
    )


def get_unix_diff_per_name(data):
    return [
        [reviews[0], count_deltatime(reviews[1])]
        if len(reviews[1]) > 1
        else [reviews[0], ("single_review", "single_review", "single_review")]
        for reviews in data.items()
    ]


def get_potential_bots(data):
    return set(map(lambda comment: comment[0] if comment[1][0] == 0 else None, data))


def filter_bot_review(data, potential_bots):

    analyzed_data = {
        reviewerID: reviews
        for reviewerID, reviews in data.items()
        if reviewerID not in potential_bots
    }

    number_of_bot_comments = sum(
        [
            len(reviews)
            for reviewerID, reviews in data.items()
            if reviewerID in potential_bots
        ]
    )
    return analyzed_data, number_of_bot_comments


def process_data(data):

    unix_diff_per_name = get_unix_diff_per_name(data)

    potential_bots = get_potential_bots(unix_diff_per_name)

    analyzed_data, number_of_bot_comments = filter_bot_review(data, potential_bots)
    return analyzed_data, potential_bots, number_of_bot_comments


def analize_bots_comments(data):

    all_potential_bots = set()
    all_number_of_bot_comments = 0
    all_analyzed_data = {}

    for (analyzed_data, potential_bots, number_of_bot_comments) in run_func_parallel(
        process_data, run_func_parallel(prepare_data, data)
    ):
        all_potential_bots.update(potential_bots)
        all_number_of_bot_comments += number_of_bot_comments
        for reviewer, reviews in analyzed_data.items():
            all_analyzed_data.setdefault(reviewer, []).extend(reviews)

    # analize_bots_comments_in_concatenated_data
    processing_data, additional_number_of_bot_comments = filter_bot_review(
        all_analyzed_data, all_potential_bots
    )
    all_number_of_bot_comments += additional_number_of_bot_comments
    sorted_processing_data = {
        reviewer: sorted(reviews, key=lambda review: review.time)
        for reviewer, reviews in all_analyzed_data.items()
    }
    return sorted_processing_data, all_number_of_bot_comments


def get_nearest_reviews(data):
    sorted_processing_data, all_number_of_bot_comments = analize_bots_comments(data)
    analyzed_data, potential_bots, number_of_bot_comments = process_data(
        sorted_processing_data
    )
    unix_diff_per_name = get_unix_diff_per_name(analyzed_data)
    nearest_reviews = min(
        [review for review in unix_diff_per_name if review[1][1] != "single_review"],
        key=lambda review: review[1][0],
    )
    return nearest_reviews, all_number_of_bot_comments
