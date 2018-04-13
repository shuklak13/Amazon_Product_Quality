# Description of Project

Our project is based off the paper ["A Probabilistic Graphical Model for Brand Reputation Assessment in Social Networks"](https://dl.acm.org/citation.cfm?id=2492556), written by researchers at Northwestern University and presented at the 2013 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining. The paper proposes a probabilistic graphical model to measure "social brand reputation", a metric of how positively or negatively a "brand" is perceived on a social network. The paper uses a Facebook dataset, where "brands" include public pages, such as Barach Obama or Starbucks. Along with social brand reputation, the proposed model computes "user positivities", a metric of how positive or negative a user's posts are on the social network. Both social brand reputation and user positivities are modeled as hidden variables whose values are inferred from the sentiment of social media posts, which act as the observed variable. The inference is conducted via Markov Chain Monte Carlo sampling.

We aim to produce a similar model to the one described in the paper on an Amazon product review dataset. This dataset is a good fit, because just like in a social network, Amazon has "brands" (products) with "reputations" (5-star ratings) determined by "posts" (reviews) from "users". We can evaluate our model's success by comparing each product's "social brand reputation" with their real Amazon rating.

This model computes P(R|S) and P(U|S), where R is a brand's reputation or a product's rating, U is user positivity, and S is the sentiment of posts or reviews. The model does not compute P(R|U), the probability of a particular user liking a product. In other words, this model only computes the "aggregate" quality of a product, given a corpus of reviews. This model is not a recommendation system. It would be interesting to explore the use of MCMC models in recommendation systems in the future.

Sentiment analysis is performed by the [Textblob](http://textblob.readthedocs.io/en/dev/index.html) package, which wraps around the [pattern](https://www.clips.uantwerpen.be/pages/pattern-en#sentiment) package created by the CLiPS research center at the University of Antwerp. The sentiment analysis is performed by assigning a sentiment polarity to every adjective in the text and averaging all of the adjective sentiments. This is a very simple model; more advanced models could be trained and tested on [the Amazon Reviews for Sentiment Analysis dataset](https://www.kaggle.com/bittlingmayer/amazonreviews). For simplicity, we assume that Textblob's false positive rate and false negative rate are approximately equal, so that the predicted rating for any given product is not impacted by errors in Textblob's sentiment prediction.

[The original paper](https://dl.acm.org/citation.cfm?id=2492556) uses a much more involved ensemble sentiment analysis algorithm that we excluded in our model due to time constraints. The original paper also has an involved data cleaning phase that filters out brands and users with very few posts, as well as users with too many posts (spammers). We did not include this phase.


# Mathematics and Time Complexity of the Model

## Brute Force

A naive, brute force inference of reputation of brands (R) and positivity of users (U) given the sentiment of comments/reviews (S) can be seen below.

![Probability of R given S](https://github.com/shuklak13/Amazon_Product_Quality/blob/master/images/P_R_given_S.JPG "Probability of R given S)

Assume that there are m brands and n users. Then there are 2^(m+n) possible combinations of brand and user positivities. For each combination, we need to sum the probability of sentiment for each review. The number of reviews could be up to mn (one review per user-brand tuple). So, in total, the brute force computation could take O(mn * 2^(m+n)) time.

## Markov Chain Monte Carlo

In this approach, we iteratively sample a positivity for every brand R and every user U, using the previous sample's positivities as well as the sentiments of the reviews. The inference equations can be seen below.

![Probability of MCMC](https://github.com/shuklak13/Amazon_Product_Quality/blob/master/images/P_MCMC.JPG_"Probability of MCMC)

As we can see, each brand's probability of positivity is independent of all other brands. We must take the product of all reviews in S belonging to a particular brand in R, and we must sum up over both possible values of a brand reputation (positive or negative, so only 2 values). So, the computation of a single brand's reputation in a single iteration of MCMC should be O(n), for the possible number of users who reviewed the product. Since there are m products, the total time complexity should be O(mni), where i is the number of iterations.


# Extra Variables

Our application computes a "reputation" for every product given the text of reviews that users provide on products. In reality, Amazon already has a metric for this - 5-star ratings. Given the 5-star rating system with adequate spam detection, a reputation inference system may not be useful. Nevertheless, it is interesting to predict a product's reputation exclusively using text. This model could integrated into an ensemble model recommendation system, and we could expand the Markov field to include other variables to inference, such as the popularity of certain genres or the reputation of different retailers.


# Data

We received our data from the [University of California San Diego's Amazon dataset](http://jmcauley.ucsd.edu/data/amazon/). In particular, the dataset we used was "reviews_Amazon_Instant_Video_5.json.gz", a set of reviews for Amazon Instant Video content, but our technique should work on any of the 5-core datasets they provided.


# Code Execution

1. Run `python parse.py [-d=<data_file>] [-p=<product_pickle_file>] [-u=<user_pickle_file>] [-s=<sentiment_pickle_file>]` to parse the input dataset (which must be stored in a file of type `.json.gz`). The data is processed and stored in three Python dictionaries - `product_pickle_file` is a mapping between each product and its reviews, `user_pickle_file` is a mapping between each user and his or her reviews, and `sentiment_pickle_file` is a mapping between each user-product tuple and the sentiment of the corresponding review. These dictionaries are stored in pickle files. The defaults are "reviews_Amazon_Instant_Video_5.json.gz", "products.pkl", "users.pkl", and "sentiments.pkl". This step only needs to be run once per dataset.
2. Run `python sample.py [-p=<product_pickle_file>] [-u=<user_pickle_file>] [-s=<sentiment_pickle_file>] [-r=<rounds>]` to run a MCMC sampling for the specified number of rounds to predict the probability that each product is "of quality". The default files are the same as parse.py. The default number of rounds is 100.
3. Run `python evaluate.py` to create a linear regression model measuring the strength of correlation between our model's output probabilities and the real Amazon 5-star score. This model could also be used as a rating-prediction score for any given user.

If you would like to run all the Python processes in a single pipeline, you can run `python pipeline.py`.


# Current Results

The below results are from a linear regression between the predicted probability that an arbitrary users would like an item, and the actual Amazon review score. This was done on 20 randomly selected products from the category "Amazon Instant Video". We manually found the videos from the Amazon Instant Video website and recorded their ratings. Not all videos in the dataset (which was from 2014) are still present on the Amazon website.


Below is the result given 10 rounds of MCMC iteration.

    LinregressResult(slope=-0.09756557841102093, intercept=4.269522551424797, rvalue=-0.21483692802155377, pvalue=0.3630327541904286, stderr=0.10454189364662447)
    
Below is the result given 20 rounds of MCMC iteration.

	LinregressResult(slope=-0.05931588494428614, intercept=4.185579165586939, rvalue=-0.11676888677816905, pvalue=0.6239466389292054, stderr=0.11891221102931385)

Below is the result given 30 rounds of MCMC iteration.

    LinregressResult(slope=-0.0787656802048556, intercept=4.229191922466046, rvalue=-0.15344701040967157, pvalue=0.51834909678057, stderr=0.1195551370112885)

    
Below is the result given 40 rounds of MCMC iteration.

    LinregressResult(slope=-0.04811300253531327, intercept=4.16148134733792, rvalue=-0.09175607765155108, pvalue=0.7004322472170617, stderr=0.12307091424238395)

It takes 30 rounds of MCMC for "convergence", where convergence is defined as the point in time where the average absolute difference between consecutive computated marginal probabilities of R becomes less than 1%.

The model's predicted rating after 40 rounds of MCMC is poorly correlated with the true 5-star ratings from Amazon Instant Video. There are multiple reasons why this could be the case. Our sentiment analysis model may have poorly predicted a review's sentiment. Our small test data sample may have been outliers in the population. Perhaps users factor in other confounding variables into their ratings that are independent of their enjoyment of the movie, such as the movie's prestige or its current Amazon rating.


# Checklist

Completed:
- [X] Sentiment Analysis
- [X] Implementation of Algorithm (for product ratings)
- [X] Evaluation (compare predicted 5-star rating to real Amazon rating by training a regression model)
- [X] Find Mixing Time
- [X] Add [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)

Next Steps
- [ ] Write up a report / demo (~4/18)
- [ ] Create a visualization demonstrating our results
  - [ ] Visualize convergence/mixing time and relate it to rounds of MCMC
  - [ ] Play around with sigma, alpha, and beta values and evaluate impact on model performance ("performance" = speed of mixing time, or accuracy of model)
- [ ] Bigger, better dataset
  - [ ] Run on larger dataset on cluster (cloud, school servers, etc.)
  - [ ] [Query real Amazon reviews to evaluate on from the Amazon API](https://python-amazon-product-api.readthedocs.io/en/latest/)
  - [ ] Manually expand Amazon dataset (manually check scores on Amazon website)
- [ ] Explore using this model in the context of recommendation systems, customer segmentation, or retail portfolio optimization