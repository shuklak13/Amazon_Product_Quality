import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pickle', help="pickle file containing parsed review data (output of parse.py)", default="products.pkl")
parser.add_argument('-r', '--rounds', help="number of rounds to iterate", default=100, type=int)
args = parser.parse_args()
print("Command-line args:" + str(args.__dict__))

import pickle
with open(args.pickle, 'rb') as f:
    products = pickle.load(f)

probability = {product: 0.5 for product in products}
sigma = 0.1 #probability that a positive user rates a positive product negatively; "noise factor"
alpha = 0.3 #probability that a positive user rates a negative product positively
beta  = 0.6 #probability that a negative user rates a positive product positively

import random
random.seed(3)
for r in range(1, args.rounds):
    for product in products:
        sample = random.random() < probability[product]     # randomly 1 or 0, based on probability
        probability[product] = (r*probability[product] + sample)/(r+1)    # (avg of n+1 items) = ((avg of n items) + new item)/(n+1)
print(probability)