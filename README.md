# Description of Project

Our project is based off the paper ["A Probabilistic Graphical Model for Brand Reputation Assessment in Social Networks"](https://dl.acm.org/citation.cfm?id=2492556), written by researchers at Northwestern University and presented at the 2013 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining. The paper proposes a probabilistic graphical model to measure "social brand reputation", a metric of how positively or negatively a "brand" is perceived on a social network. The paper uses a Facebook dataset, where "brands" include public pages, such as Barach Obama or Starbucks. Along with social brand reputation, the proposed model computes "user positivities", a metric of how positive or negative a user's posts are on the social network. Both social brand reputation and user positivities are modeled as hidden variables whose values are inferred from the sentiment of social media posts, which act as the observed variable. The inference is conducted via Markov Chain Monte Carlo sampling.

We aim to produce a similar model to the one described in the paper on an Amazon product review dataset. This dataset is a good fit, because just like in a social network, Amazon has "brands" (products) with "reputations" (5-star ratings) determined by "posts" (reviews) from "users". We can evaluate our model's success by comparing each product's "social brand reputation" with their real Amazon rating.

This model computes P(R|S) and P(U|S), where R is a brand's reputation or a product's rating, U is user positivity, and S is the sentiment of posts or reviews. The model does not compute P(R|U), the probability of a particular user liking a product. In other words, this model only computes the "aggregate" quality of a product, given a corpus of reviews. This model is not a recommendation system. It would be interesting to explore the use of MCMC models in recommendation systems in the future.

Sentiment analysis is performed by the [Textblob](http://textblob.readthedocs.io/en/dev/index.html) package, which wraps around the [pattern](https://www.clips.uantwerpen.be/pages/pattern-en#sentiment) package created by the CLiPS research center at the University of Antwerp. The sentiment analysis is performed by assigning a sentiment polarity to every adjective in the text and averaging all of the adjective sentiments. This is a very simple model; more advanced models could be trained and tested on [the Amazon Reviews for Sentiment Analysis dataset](https://www.kaggle.com/bittlingmayer/amazonreviews). For simplicity, we assume that Textblob's false positive rate and false negative rate are approximately equal, so that the predicted rating for any given product is not impacted by errors in Textblob's sentiment prediction.

[The original paper](https://dl.acm.org/citation.cfm?id=2492556) uses a much more involved ensemble sentiment analysis algorithm that we excluded in our model due to time constraints. The original paper also has an involved data cleaning phase that filters out brands and users with very few posts, as well as users with too many posts (spammers). We did not include this phase.


# Mathematics and Time Complexity of the Model

## Brute Force

A naive, brute force inference of reputation of brands (R) and positivity of users (U) given the sentiment of comments/reviews (S) can be seen below.

![Probability of R given S](https://github.com/shuklak13/Amazon_Product_Quality/blob/master/images/P_R_given_S.JPG)

Assume that there are m brands and n users. Then there are 2^(m+n) possible combinations of brand and user positivities. For each combination, we need to sum the probability of sentiment for each review. The number of reviews could be up to mn (one review per user-brand tuple). So, in total, the brute force computation could take O(mn * 2^(m+n)) time.

## Markov Chain Monte Carlo

In this approach, we iteratively sample a positivity for every brand R and every user U, using the previous sample's positivities as well as the sentiments of the reviews. The inference equations can be seen below.

![Probability of MCMC](https://github.com/shuklak13/Amazon_Product_Quality/blob/master/images/P_MCMC.JPG)

As we can see, each brand's probability of positivity is independent of all other brands. We must take the product of all reviews in S belonging to a particular brand in R, and we must sum up over both possible values of a brand reputation (positive or negative, so only 2 values). So, the computation of a single brand's reputation in a single iteration of MCMC should be O(n), for the possible number of users who reviewed the product. Since there are m products, the total time complexity should be O(mni), where i is the number of iterations.

## Priors

![Probability of MCMC](https://github.com/shuklak13/Amazon_Product_Quality/blob/master/images/Priors.JPG)

The probabilities P(S|U,R) are dependent on priors alpha, beta, and delta (referred to as "gamma" below).

* "Alpha"=`P(S=1 | U=1, R=0)` is the probability that a positive user rates a negative product positively. It can be interpreted as the strength of a user's positivity on a review's rating.
* "Beta"=`P(S=1 | U=0, R=1)` is the probability that a negative user rates a positive product positively. It can be interpreted as the strength of a product's quality on a review's rating.
* "Gamma"=`P(S=0 | U=1, R=1)` is the probability that a positive user rates a positive product negatively. It can be interpreted as a "noise factor".

The paper makes the assumption that `Alpha<Beta` (the product's quality has a greater impact on a review's rating than the user's positivity). However, the paper provides no justificaiton for this assumption, so we ignored it in our analysis.

The values used in the paper are alpha=0.3, beta=0.6, and gamma=0.1, which we used as a "control" or "baseline" for the model. We compared the performance of the model using three alternative parameter configurations (increasing alpha, decreasing beta, and increasing gamma).


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

The below results are from a linear regression between the predicted probability that an arbitrary users would like an item, and the actual Amazon review score. This was done on 708 scraped products from the category "Office Supplies". Not all products in the dataset (which was from 2014) are still present on the Amazon website.


Below is the result given 10 rounds of MCMC iteration.

    LinregressResult(slope=0.015109064081682277, intercept=3.9670587003455151, rvalue=0.049427499036819499, pvalue=0.18896087229517064, stderr=0.011490407201475823)

We had a correlation coefficient of `0.0494274990368`.

It takes 30 rounds of MCMC for "convergence", where convergence is defined as the point in time where the average absolute difference between consecutive computated marginal probabilities of R becomes less than 1%.

The model's predicted rating after 40 rounds of MCMC is poorly correlated with the true 5-star ratings from Amazon Instant Video. There are multiple reasons why this could be the case. Our sentiment analysis model may have poorly predicted a review's sentiment. Our small test data sample may have been outliers in the population. Perhaps users factor in other confounding variables into their ratings that are independent of their enjoyment of the movie, such as the movie's prestige or its current Amazon rating.

## Scatter Plot

![Scatterplot](https://github.com/shuklak13/Amazon_Product_Quality/blob/master/images/scatterplot.png)

## Test Cases:

1. For sigma = 0.1, alpha = 0.3, beta =  0.6
    -   10 rounds, correlation is 0.0317650552114
    -   20 rounds, correlation is 0.0347479106453
    -   30 rounds, correlation is 0.0351023571345
    -   40 rounds, correlation is 0.0337202571689
    -   100 rounds, correlation is 0.0360805236603
2. For sigma = 0.5, alpha = 0.5, beta =  0.5
    -   10 rounds, correlation is 0.0317650552114
    -   20 rounds, correlation is 0.0273848647798
    -   30 rounds, correlation is 0.00285424424937
    -   40 rounds, correlation is 0.0128539720687
    -   50 rounds, correlation is 0.0270753175784
3. For sigma = 0.2, alpha = 0.2, beta =  0.8
    -   10 rounds, correlation is 0.0367868565372
    -   20 rounds, correlation is 0.0419762437656
    -   30 rounds, correlation is 0.0411693830939
    -   40 rounds, correlation is 0.0400037235887
4. For sigma = 0.7, alpha = 0.9, beta =  0.3
    -   10 rounds, correlation is 0.0350938772052
    -   20 rounds, correlation is 0.0444470982371
    -   30 rounds, correlation is 0.044057186709
    -   40 rounds, correlation is 0.0227733827952


## Performance Evaluation

One of the common aspects related to MCMC- based inference algorithm with respect to performance evaluation is time complexity of sampling. To address this, we parallelize block-based MCMC due to conditional independency and compare to sequential version in terms of time taken. Speedup is a very common metric used in the field of parallelism. Speedup is determined as a ratio of time taken in a sequential algorithm to time taken in parallel algorithm with p processors. We are using 8 processors in parallel. 

![Speedup Results](https://github.com/shuklak13/Amazon_Product_Quality/blob/master/images/speedUp.png)
   
          

# Checklist

Completed:
- [X] Sentiment Analysis
- [X] Implementation of Algorithm (for product ratings)
- [X] Evaluation (compare predicted 5-star rating to real Amazon rating by training a regression model)
- [X] Find Mixing Time
- [X] Add [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [X] Write up a report / demo (~4/18)
- [X] Create a visualization demonstrating our results
  - [X] Visualize convergence/mixing time and relate it to rounds of MCMC
  - [X] Play around with sigma, alpha, and beta values and evaluate impact on model performance ("performance" = speed of mixing time, or accuracy of model)
- [X] Bigger, better dataset
  - [ ] Run on larger dataset on a cluster (AWS cloud, school servers, etc.)
  - [X] [Query real Amazon reviews to evaluate on from the Amazon API](https://python-amazon-product-api.readthedocs.io/en/latest/)

Next Steps / Stretch Goals
- [ ] Explore using this model in the context of recommendation systems, customer segmentation, or retail portfolio optimization
