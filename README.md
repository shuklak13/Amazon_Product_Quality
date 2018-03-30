# Data

We received our data from the [University of California San Diego's Amazon dataset](http://jmcauley.ucsd.edu/data/amazon/). In particular, the dataset we used was "reviews_Amazon_Instant_Video_5.json.gz", a set of reviews for Amazon Instant Video content, but our technique should work on any of the 5-core datasets they provided.


# Code Execution

1. Run "python parse.py (data_file) (pickle_file)" to parse the data file into a Python dictionary, which is stored in a pickle file. The defaults are "reviews_Amazon_Instant_Video_5.json.gz" and "products.pkl". This step only needs to be run once per dataset.
2. Run "python sample.py (pickle_file) (rounds)" to run a MCMC sampling for the specified number of rounds to predict the probability that each product is "of quality". The defaults are "products.pkl" and 100.
3. Run "python evaluate.py" to create a linear regression model measuring the strength of correlation between our model's output probabilities and the real Amazon 5-star score. This model could also be used as a rating-prediction score for any given user.


# Current Results

The below results are from a linear regression betweeen the predicted probability that an arbitrary users would like an item, and the actual Amazon review score. This was done on 20 products.

    LinregressResult(slope=0.53754379740098479, intercept=3.8027298531955478, rvalue=0.2402211636806181, pvalue=0.30764972157693871, stderr=0.51198766872208323)


# Checklist

Completed:
- [X] Sentiment Analysis
- [X] Implementation of Algorithm (for product ratings)
- [X] Evaluation (compare predicted 5-star rating to real Amazon rating by training a regression model)

Next Steps:
- [ ] Fix probability calculation (sample.py line 12)
- [ ] Calculate+print User General Sentiment, + incorporate user general sentiment into current probability calculations

Later:
- [ ] [Query real Amazon reveiws to evaluate on](https://python-amazon-product-api.readthedocs.io/en/latest/)
- [ ] Expand Amazon dataset (manually check scores on Amazon website)
- [ ] Write up a report / demo / presentation
- [ ] Add [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)