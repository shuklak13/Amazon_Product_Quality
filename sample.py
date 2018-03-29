import sys
pkl_path = sys.argv[1] if len(sys.argv)>1  else "products.pkl"
try:
    import pickle
    with open(pkl_path, 'rb') as f:
        products = pickle.load(f)
except FileNotFoundError:
    print(pkl_path + " doesn't exist.")
    pkl_path = "products.pkl"
    from parse import products

prob_vector = {product: 0.5 for product in products}
sumProbs = {product: 0.5 for product in products}
numRounds = 50
sigma = 0.1 #probability that a positive user rates a positive product negatively
alpha = 0.3 #probability that a positive user rates a negative product positively
beta  = 0.6 #probability that a negative user rates a positive product positively

from random import random
for rnd in range(1, numRounds):
    sample = {product: random() < prob_vector[product] for product in products}
    sumProbs = {product: sumProbs[product]+sample[product] for product in products}
    prob_vector = {product: sumProbs[product]/rnd for product in products}
print(prob_vector)