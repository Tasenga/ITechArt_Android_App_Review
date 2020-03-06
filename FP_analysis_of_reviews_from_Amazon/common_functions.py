import concurrent.futures
from itertools import groupby
from dataclasses import dataclass

def run_func_parallel(func, data):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return [it for it in executor.map(func, data)]

@dataclass
class AppScore:
    asin: str
    total_score: float = 0.0
    number_of_votes: int = 0
    @property
    def average_score(self):
        return round(self.total_score / self.number_of_votes, 2)

def get_apps_scores(data):
    """
    function returns a dictionary where keys are asins,
    value is a list of scores.
    """
    return {
        key: [group["overall"] for group in groups if "overall" in group.keys()]
        for key, groups in groupby(
            sorted(data, key=lambda position: position["asin"]),
            key=lambda position: position["asin"])
    }

def get_dict_of_apps_with_score(data):
    apps_scores = {}
    for result in run_func_parallel(get_apps_scores, data):
        for asin, list_of_scores in result.items():
            app_score_obj = apps_scores.setdefault(asin, AppScore(asin, 0, 0))
            app_score_obj.total_score += sum(list_of_scores)
            app_score_obj.number_of_votes += len(list_of_scores)
    return apps_scores