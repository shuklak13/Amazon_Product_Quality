import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pickle', help="pickle file containing parsed review data (output of parse.py)", default="products.pkl")
parser.add_argument('-r', '--rounds', help="number of rounds to iterate", default=100, type=int)
args = parser.parse_args()
print("Command-line args:" + str(args.__dict__))

import pickle
with open(args.pickle, 'rb') as f:
    R = pickle.load(f)

# parameters determining the distribution P(R,U|S)
sigma = 0.1 #probabilities that a positive user rates a positive product negatively; "noise factor"
alpha = 0.3 #probabilities that a positive user rates a negative product positively
beta  = 0.6 #probabilities that a negative user rates a positive product positively


def sample():   # TO-DO: USE EQUATION 2 FOR SAMPLING
    global random
    return random()>0.5     # THIS IS A PLACEHOLDER

from random import seed, random
seed(3)
prob_R = {product: 0.5 for product in R}
for k in range(1, args.rounds):
    for i in R:
        sample_R_i = sample()   # draw sample
        prob_R_i = (prob_R[i]) if sample_R_i else (1-prob_R[i]) # probability of drawing that sample
        R_i_k = prob_R_i >= random()    # rejection sampling
        prob_R[i] = (k*prob_R[i] + R_i_k)/(k+1)    # update probability based on sample
print(prob_R)

product_probabilities_pkl = "product_probabilities.pkl"
with open(product_probabilities_pkl, 'wb') as f:
    pickle.dump(prob_R, f)
print("Parsed review data stored in " + product_probabilities_pkl)