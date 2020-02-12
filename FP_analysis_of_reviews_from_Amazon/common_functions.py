import concurrent.futures
from itertools import groupby


class AppScore:
    def __init__(self, asin, total_score, number_of_votes):
        self.asin = asin
        self.total_score = total_score
        self.number_of_votes = number_of_votes
    @property
    def average_score(self):
        return round(self.total_score / self.number_of_votes, 2)

def calculate_app_score(item):
    asin = item[0]
    list_of_scores = tuple(map(lambda x: x["overall"], item[1]))
    total_score = sum(list_of_scores)
    number_of_votes = len(list_of_scores)
    app_score_obj = AppScore(asin, total_score, number_of_votes)
    return app_score_obj

def get_apps_scores(data):
    """
    function returns a dictionary where keys are asins,
    value is a list of scores.
    """
    grouped_analyzed_data = groupby(
            sorted(data, key=lambda review: review["asin"]),
            key=lambda review: review["asin"]
        )

    part_of_apps_scores = tuple(map(calculate_app_score, grouped_analyzed_data))
    return part_of_apps_scores

def get_apps_scores_parallel(*args):
    """
    function runs several processes to implement function 'get_asins_score' and to combine results this function.
    Returns a dictionary where keys are asins, values are total score and number of votes per asin.
    """
    apps_scores = ()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for part_of_apps_scores in executor.map(get_apps_scores, args):
            apps_scores += part_of_apps_scores

    apps_scores = groupby(
            sorted(apps_scores, key=lambda app_score_obj: app_score_obj.asin),
            key=lambda app_score_obj: app_score_obj.asin,
        )
    return apps_scores

def concatenate_result(item):

    asin = item[0]
    list_of_scores_and_votes = tuple(map(lambda x: (x.total_score, x.number_of_votes), item[1]))
    total_score = sum(tuple(map(lambda x: x[0], list_of_scores_and_votes)))
    number_of_votes = sum(tuple(map(lambda x: x[1], list_of_scores_and_votes)))
    app_score_obj = AppScore(asin, total_score, number_of_votes)
    return app_score_obj