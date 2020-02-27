# Amazon apps_for_Android

This app gives following results after running py-files:
In 'analysis_of_reviews_from_Amazon' module:
1) Task_1_1.py: to create file general-stats.cvs containing information about:
              - average rating (overall) of each application (asin);
              - messages with the most “likes” from the entire data set and the application (asin) associated with it;
              - the shortest interval between ratings of one user (among all users) and the length of both messages which create this interval;
              - the application which received the most useless message;
              - the number of records that cannot be processed for every point above.
2) Task_1_2.py: to create file apps-stats.cvs containing information about average rating (overall) of each application (asin) and number of voters.
3) Task_1_3.py: to create file words-stats1.cvs и words-stats2.cvs containing information about the most popular words from positive and negative messages.

In 'analysis_of_products_in_stores' module:
1) Task_2_1.py to create file L8_result.csv containing information about:
                - number of unique products and stores;
                - the user who approved the highest number of prices;
                - the number of products sold in each store;
                - the average cost of each product;
                - shops which selling the most expensive and cheapest product (indicating the product and its price).

'FP_analysis_of_reviews_from_Amazon' module resolves the same tasks as the 'analysis_of_reviews_from_Amazon' module, but with using concurrent_future:
1) Task_9_1.py: to create file general-stats.cvs containing information about:
              - average rating (overall) of each application (asin);
              - messages with the most “likes” from the entire data set and the application (asin) associated with it;
              - the shortest interval between ratings of one user (among all users) and the length of both messages which create this interval;
              - the application which received the most useless message;
              - the number of records that cannot be processed for every point above.
2) Task_9_2.py: to create file apps-stats.cvs containing information about average rating (overall) of each application (asin) and number of voters.
3) Task_9_3.py: to create file words-stats1.cvs и words-stats2.cvs containing information about the most popular words from positive and negative messages.

In 'analysis_of_user_actions' module the following data were output with using Jupyter notebook:
    - retrieving data that can't be processed;
    - percentage of operations (pie chart);
    - the total number of operations by weeks;
    - top 10 most lengthy searching operations indicating time spent;
    - histogram of input data for each operation;
    - graph of the number of successful, conditionally successful (warning) and unsuccessful results;
    - dependence of the time spent on the amount of input data.

## Getting Started

Before start you need to get database from http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Apps_for_Android_5.json.gz and save it to 'source' folder and unpack.
To separate database you need to run 'common_module/work_with_document.py' file.
To get start you need to run corresponding file (see above).

Before start module 'analysis_of_user_actions' you need to get database from https://stlab.itechart-group.com/courses/contest/240/
To get start you need to run file 'user_actions.ipynb' with using jupyter notebook.

### Prerequisites

To running application is used:
python version
pip version-20.0.2

```
pip install -r requirements.txt
```

## Running the tests

//Explain how to run the automated tests for this system *automated tests absent*

### Break down into end to end tests

//Explain what these tests test and why *automated tests absent*

```
//Give an example *automated tests absent*
```

## Additional materials

For 'analysis_of_reviews_from_Amazon' module:
Using database is received from: http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Apps_for_Android_5.json.gz
Description of data is received from: http://jmcauley.ucsd.edu/data/amazon/

For 'analysis_of_user_actions' module:
Using database is received from: https://stlab.itechart-group.com/courses/contest/240/

## Versioning

Version history:
2019.02.01 - v.1.0.0. - current version

## Authors

Anastasia Orlovskaya - (e_mail: nastassia.orlovskaya@gmail.com)
