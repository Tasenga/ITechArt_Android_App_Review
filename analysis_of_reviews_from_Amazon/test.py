from itertools import groupby

dict = {
    reviewID: sorted(reviews, key=lambda review: review['unixReviewTime'])
    for reviewID, reviews
    in groupby(sorted(main_dict.values(), key=lambda review: review['reviewerID']),
               key=lambda review: review['reviewerID'])
}