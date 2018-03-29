import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pickle', help="pickle file containing parsed review data (output of parse.py)", default="products.pkl")
parser.add_argument('-r', '--rounds', help="iumber of rounds to iterate", default=100, type=int)
args = parser.parse_args()
print("Command-line args:" + str(args.__dict__))

import pickle
pkl_path = args.pickle
with open(pkl_path, 'rb') as f:
    products = pickle.load(f)

prob_vector = {product: 0.5 for product in products}
sumProbs = {product: 0.5 for product in products}
numRounds = args.rounds
sigma = 0.1 #probability that a positive user rates a positive product negatively
alpha = 0.3 #probability that a positive user rates a negative product positively
beta  = 0.6 #probability that a negative user rates a positive product positively

from random import random
for rnd in range(1, numRounds):
    sample = {product: random() < prob_vector[product] for product in products}
    sumProbs = {product: sumProbs[product]+sample[product] for product in products}
    prob_vector = {product: sumProbs[product]/rnd for product in products}
print(prob_vector)