# Data

We received our data from the [University of California San Diego's Amazon dataset](http://jmcauley.ucsd.edu/data/amazon/). In particular, the dataset we used was "reviews_Amazon_Instant_Video_5.json.gz", a set of reviews for Amazon Instant Video content, but our technique should work on any of the 5-core datasets they provided.


# Code Execution

1. Run "python parse.py (data_file) (pickle_file)" to parse the data file into a Python dictionary, which is stored in a pickle file. The default names are "reviews_Amazon_Instant_Video_5.json.gz" and "products.pkl". This step only needs to be run once per dataset.
2. Run "python sample.py (pickle_file)" to ...???. The default pickle file is "products.pkl".


# Checklist

- [X] Sentiment Analysis
- [X] Implementation of Algorithm (for product ratings)
- [ ] Convert probability output into an Amazon-style 5-star rating
- [ ] Evaluation (compare predicted 5-star rating to real Amazon rating by training a regression model)
- [ ] [Query real Amazon reveiws to evaluate on](https://python-amazon-product-api.readthedocs.io/en/latest/)
- [ ] Write up a report / demo / presentation
- [ ] Add [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [ ] Calculate user ratings (just print them out I guess? IDK what to use them for)