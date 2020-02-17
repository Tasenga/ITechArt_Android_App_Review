import concurrent.futures
from itertools import groupby


def run_func_parallel(func, data):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return [it for it in executor.map(func, data)]


class AppScore:
    def __init__(self, asin, total_score, number_of_votes):
        self.asin = asin
        self.total_score = total_score
        self.number_of_votes = number_of_votes
    @property
    def average_score(self):
        return round(self.total_score / self.number_of_votes, 2)

def get_apps_scores(data):
    """
    function returns a dictionary where keys are asins,
    value is a list of scores.
    """
    return {
        key: [group["overall"] for group in groups]
        for key, groups in groupby(
            sorted(data, key=lambda position: position["asin"]),
            key=lambda position: position["asin"],
        )
    }

def get_dict_of_apps_with_score(data):
    apps_scores = {}
    for result in run_func_parallel(get_apps_scores, data):
        for asin, list_of_scores in result.items():
            app_score_obj = apps_scores.setdefault(asin, AppScore(asin, 0, 0))
            app_score_obj.total_score += sum(list_of_scores)
            app_score_obj.number_of_votes += len(list_of_scores)
    return apps_scores