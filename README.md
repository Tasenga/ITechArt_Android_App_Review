# Amazon apps_for_Android

This app gives following results after running py-files:
In 'analysis of reviews from Amazon' module:
1) Task_1.py: to create file general-stats.cvs containing information about:
              - average rating (overall) of each application (asin);
              - messages with the most “likes” from the entire data set and the application (asin) associated with it;
              - the shortest interval between ratings of one user (among all users) and the length of both messages which create this interval;
              - the application which received the most useless message;
              - the number of records that cannot be processed for every point above.
2) Task_2.py: to create file apps-stats.cvs containing information about average rating (overall) of each application (asin) and number of voters.
3) Task_3.py: to create file words-stats1.cvs и words-stats2.cvs containing information about the most popular words from positive and negative messages.

In 'analysis of products in stores' module:
1) Task_1.py to create file common-info.cvs containing information about:
                - number of unique products and stores;
                - the user who approved the highest number of prices;
                - the number of products sold in each store;
                - the average cost of each product;
                - shops which selling the most expensive and cheapest product (indicating the product and its price).

## Getting Started

Before start you need to get database from http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Apps_for_Android_5.json.gz and save it to 'source' folder.
To get start you need to run corresponding file (see above).

To configure local git hooks you need:
  - to save all files from directory './git.hooks' folder to directory './.git/hooks/';
  - to input command 'chmod +x <file_name>' per file in git.bush terminale in root directory.

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

Using database is received from: http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Apps_for_Android_5.json.gz
Description of data is received from: http://jmcauley.ucsd.edu/data/amazon/


## Versioning

Version history:
2019.02.01 - v.1.0.0. - current version

## Authors

Anastasia Orlovskaya - (e_mail: nastassia.orlovskaya@gmail.com)
