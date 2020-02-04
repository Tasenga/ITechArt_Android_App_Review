from source import get_data
from document_creation import file_create

def avg_rating(main_dict):
    '''function returns an average rating of each application and number of voters

    2.1. Task_2.py: to create file apps-stats.cvs containing information about
    average rating (overall) of each application (asin) and number of voters.
    '''
    asins = []
    for item in main_dict.values():
        asins.append(item['asin'])
    asins_value = dict.fromkeys(set(asins), [0, 0])
    for item in main_dict.values():
        asins_value[item['asin']] = [asins_value.get(item['asin'])[0] + item['overall'], asins_value.get(item['asin'])[1]+1]
    avg_overall = []
    for key, value in asins_value.items():
        avg_overall.append([
            key,
            str(round(asins_value.get(key)[0] / asins_value.get(key)[1], 2)).replace('.', ','),
            asins_value.get(key)[1]
        ])
    return avg_overall

if __name__ == "__main__":
    main_dict = get_data.open_gzip()
    file_create().save_file('apps-stats.cvs', avg_rating(main_dict))