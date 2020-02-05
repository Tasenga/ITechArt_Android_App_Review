from source import get_data
from document_creation import save_file

from Task_1 import avg_rating
# '''function avg_rating returns an average rating of each application and number of voters
#
# 2.1. Task_2.py: to create file apps-stats.cvs containing information about
# average rating (overall) of each application (asin) and number of voters.'''

if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    save_file('apps-stats.cvs', avg_rating(main_dict))
