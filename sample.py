# Import and Initialize
import argparse, pickle
from random import seed, random

# Read-in Command-Line Arguments
cmdlnparser = argparse.ArgumentParser()
cmdlnparser.add_argument('-p', '--productpickle', help="pickle file containing dictionary mapping each product to its reviews (input)", default="products.pkl")
cmdlnparser.add_argument('-u', '--userpickle', help="pickle file containing dictionary mapping each user to his or her reviews (input)", default="users.pkl")
cmdlnparser.add_argument('-s', '--sentimentpickle', help="pickle file containing dictionary mapping each product-user tuple to its sentiment score (input)", default="sentiments.pkl")
cmdlnparser.add_argument('-r', '--rounds', help="number of rounds to iterate for MCMC", default=100, type=int)
args = cmdlnparser.parse_args()
print("Command-line args:" + str(args.__dict__))

# Load products (R) and users (U)
with open(args.productpickle, 'rb') as f:
    R = pickle.load(f)
with open(args.userpickle, 'rb') as f:
    U = pickle.load(f)
with open(args.sentimentspickle, 'rb') as f:
    S = pickle.load(f)

# Parameters determining the distribution P(R,U|S)
sigma = 0.1 #probabilities that a positive user rates a positive product negatively; "noise factor"
alpha = 0.3 #probabilities that a positive user rates a negative product positively
beta  = 0.6 #probabilities that a negative user rates a positive product positively

# Sample from P(A_i | A_(-i), B, S)
def sample(A, i, B, S):   # TO-DO: USE EQUATION 2 FOR SAMPLING
    global random
    return random()>0.5     # THIS IS A PLACEHOLDER

# MCMC Sampling Algorithm
seed(3)
prob_R = {product: 0.5 for product in R}
for k in range(1, args.rounds):
    for i in R:
        sample_R_i = sample(R, i, U, S)   # draw sample
        prob_R_i = (prob_R[i]) if sample_R_i else (1-prob_R[i]) # probability of drawing that sample
        R_i_k = prob_R_i >= random()    # rejection sampling
        prob_R[i] = (k*prob_R[i] + R_i_k)/(k+1)    # update probability based on sample
print(prob_R)

# Store prob_R and prob_U in pickle files
product_probabilities_pkl = "product_probabilities.pkl"
with open(product_probabilities_pkl, 'wb') as f:
    pickle.dump(prob_R, f)
print("Parsed review data stored in " + product_probabilities_pkl)