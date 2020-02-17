from source.get_data import get_data
from document_creation import save_file
from common_functions import avg_rating


if __name__ == "__main__":
    main_dict = get_data('Apps_for_Android_5.json')
    save_file('apps-stats.cvs', avg_rating(main_dict))