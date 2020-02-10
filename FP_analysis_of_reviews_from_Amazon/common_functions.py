from common_functions.work_with_document import get_data_from_json
from time import time
import concurrent.futures
from multiprocessing import Pool


def asins_value(main_dict):
    asins_value = {}
    for item in main_dict:
        overall, count = asins_value.get(item['asin'], [0, 0])
        asins_value[item['asin']] = [overall + item['overall'], count + 1]
    return asins_value

def concurrent_future_get_data():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(
            get_data_from_json,
            [
                (modulename, 'part1_Apps_for_Android_5.json'),
                (modulename, 'part2_Apps_for_Android_5.json'),
                (modulename, 'part3_Apps_for_Android_5.json'),
                (modulename, 'part4_Apps_for_Android_5.json')
            ]
        )

def concurrent_future_asins_value():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(asins_value, [data1, data2, data3, data4])

def main_multiprocessing():
    with Pool(processes=4) as pool:
        pool.map(asins_value, [data1, data2])


if __name__ == '__main__':
    modulename = 'FP_analysis_of_reviews_from_Amazon'

    tic = time()
    data1 = get_data_from_json(modulename, 'part1_Apps_for_Android_5.json')
    data2 = get_data_from_json(modulename, 'part2_Apps_for_Android_5.json')
    data3 = get_data_from_json(modulename, 'part3_Apps_for_Android_5.json')
    data4 = get_data_from_json(modulename, 'part4_Apps_for_Android_5.json')
    toc = time()
    print(toc - tic)

    tic = time()
    concurrent_future_get_data()
    toc = time()
    print(toc - tic)

    tic = time()
    asins_value(data1)
    asins_value(data2)
    toc = time()
    print(toc - tic)

    tic = time()
    concurrent_future_asins_value()
    toc = time()
    print(toc - tic)

    tic = time()
    main_multiprocessing()
    toc = time()
    print(toc - tic)

