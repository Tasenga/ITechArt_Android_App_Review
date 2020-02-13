from itertools import groupby
from concurrent.futures import ProcessPoolExecutor

class ReviewTimeInfo:
    def __init__(self, time, text):
        self.time = time
        self.text = text

def prepare_data(data):
    sorted_data = {
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
    return sorted_data

def count_deltatime(data):
    min_deltatime = min(
        (data[i].time - data[i - 1].time, data[i].text, data[i - 1].text)
        for i in range(1, len(data))
    )
    return min_deltatime

def get_unix_diff_per_name(data):
    unix_diff_per_name = tuple(
        map(
            lambda reviews: [reviews[0], count_deltatime(reviews[1])]
            if len(reviews[1]) > 1
            else [reviews[0], ("single_review", "single_review", "single_review")],
            data.items(),
        )
    )
    return unix_diff_per_name

def get_potential_bots(data):
    potential_bots = set(
        map(lambda comment: comment[0] if comment[1][0] == 0 else None, data)
    )
    return potential_bots

def filter_bot_review(data, potential_bots):
    analyzed_data = dict(
        filter(lambda review: review[0] not in potential_bots, data.items())
    )
    number_of_bot_comments = sum(
        map(
            lambda reviews: len(reviews),
            dict(
                filter(lambda review: review[0] in potential_bots, data.items())
            ).values(),
        )
    )
    return analyzed_data, number_of_bot_comments

def process_data(data):

    unix_diff_per_name = get_unix_diff_per_name(data)

    potential_bots = get_potential_bots(unix_diff_per_name)

    analyzed_data, number_of_bot_comments = filter_bot_review(data, potential_bots)
    return analyzed_data, potential_bots, number_of_bot_comments

def get_nearest_review(data):
    nearest_comments = min(
        list(filter(lambda review: review[1][1] != "single_review", data)),
        key=lambda review: review[1][0],
    )
    return nearest_comments

def get_processing_data_parallel(*args):
    list_prepared_data = []
    all_potential_bots = []
    all_number_of_bot_comments = 0
    all_analyzed_data = {}
    with ProcessPoolExecutor() as executor:
        for prepared_data in executor.map(prepare_data, args):
            list_prepared_data.append(prepared_data)
    with ProcessPoolExecutor() as executor:
        for analyzed_data, potential_bots, number_of_bot_comments in executor.map(
            process_data, list_prepared_data
        ):
            all_potential_bots += potential_bots
            all_number_of_bot_comments += number_of_bot_comments
            for reviewer, reviews in analyzed_data.items():
                list_of_review = all_analyzed_data.setdefault(reviewer, [])
                list_of_review.extend(reviews)
    set_all_potential_bots = set(all_potential_bots)
    processing_data, additional_number_of_bot_comments = filter_bot_review(
        all_analyzed_data, set_all_potential_bots
    )
    all_number_of_bot_comments += additional_number_of_bot_comments
    sorted_processing_data = {
        reviewer: sorted(reviews, key=lambda review: review.time)
        for reviewer, reviews in all_analyzed_data.items()
    }
    return sorted_processing_data, all_number_of_bot_comments