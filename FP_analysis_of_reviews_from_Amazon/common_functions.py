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

def get_apps_scores(data):
    """
    function returns a dictionary where keys are asins,
    value is a list of scores.
    """
    part_of_apps_scores = {
        key: [group["overall"] for group in groups]
        for key, groups in groupby(
            sorted(data, key=lambda position: position["asin"]),
            key=lambda position: position["asin"],
        )
    }
    return part_of_apps_scores

def get_apps_scores_parallel(*args):
    """
    function runs several processes to implement function 'get_asins_score' and to combine results this function.
    Returns a dictionary where keys are asins, values are total score and number of votes per asin.
    """
    apps_scores = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for part_of_apps_scores in executor.map(get_apps_scores, args):
            for asin, list_of_scores in part_of_apps_scores.items():
                app_score_obj = apps_scores.setdefault(asin, AppScore(asin, 0, 0))
                app_score_obj.total_score += sum(list_of_scores)
                app_score_obj.number_of_votes += len(list_of_scores)
    return apps_scores

# ANOTHER WAY
#
# def get_apps_scores(data):
#     """
#     function returns a dictionary where keys are asins,
#     values are total score and number of votes per asin.
#     """
#     part_of_apps_scores = tuple(
#         map(
#             lambda app_score_obj:
#             AppScore(app_score_obj["asin"], app_score_obj["overall"], 1),
#         data)
#     )
#     return part_of_apps_scores
#
# def get_apps_scores_parallel(*args):
#     """
#     function runs several processes to implement function 'get_asins_score' and to combine results this function.
#     Returns a dictionary where keys are asins, values are total score and number of votes per asin.
#     """
#     apps_scores = ()
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         for part_of_apps_scores in executor.map(get_apps_scores, args):
#             apps_scores += part_of_apps_scores
#     return apps_scores
#
# def concatenate_apps_scores(apps_scores):
#     concatenated_list_apps_scores = [
#             [asin, [group.total_score for group in groups]]
#             for asin, groups in groupby(
#                 sorted(apps_scores, key=lambda app_score_obj: app_score_obj.asin),
#                 key=lambda app_score_obj: app_score_obj.asin,
#             )
#     ]
#     result_list_of_app_score_obj = tuple(
#         map(
#             lambda app: AppScore(app[0], sum(app[1]), len(app[1])),
#             concatenated_list_apps_scores
#         )
#     )
#     return result_list_of_app_score_obj
