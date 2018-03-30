import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pickle', help="pickle file containing parsed review data (output of parse.py)", default="products.pkl")
parser.add_argument('-r', '--rounds', help="number of rounds to iterate", default=100, type=int)
args = parser.parse_args()
print("Command-line args:" + str(args.__dict__))

import pickle
with open(args.pickle, 'rb') as f:
    products = pickle.load(f)

# parameters determining the distribution P(R,U|S)
sigma = 0.1 #probabilities that a positive user rates a positive product negatively; "noise factor"
alpha = 0.3 #probabilities that a positive user rates a negative product positively
beta  = 0.6 #probabilities that a negative user rates a positive product positively

probabilities = {product: 0.5 for product in products}  # TO-DO: fix this (should NOT be 0.5 by default for all processes; we need to incorporate sentiment. Use equation 2 on page 226.)

# TO-DO: fix this (equation 2 on page 226)
def computeProbability(P, i):
    return P[i]

import random
random.seed(3)
for k in range(1, args.rounds):
    for product in products:
        sample = random.random() < computeProbability(probabilities, product)     # randomly 1 or 0, based on probabilities
        probabilities[product] = (r*probabilities[product] + sample)/(k+1)    # (avg of n+1 items) = ((avg of n items) + new item)/(n+1)
print(probabilities)

product_probabilities_pkl = "product_probabilities.pkl"
with open(product_probabilities_pkl, 'wb') as f:
    pickle.dump(products, f)
print("Parsed review data stored in " + product_probabilities_pkl)