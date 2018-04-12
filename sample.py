# Import and Initialize
import argparse, pickle
from random import seed, random
from draw import draw_and_sample
from auxiliary import prob, avg_of_abs_diffs
from copy import deepcopy    
import time

# Read-in Command-Line Arguments
cmdlnparser = argparse.ArgumentParser()
cmdlnparser.add_argument('-p', '--productpickle', help="pickle file containing dictionary mapping each product to its reviews (input)", default="pkl/products.pkl")
cmdlnparser.add_argument('-u', '--userpickle', help="pickle file containing dictionary mapping each user to his or her reviews (input)", default="pkl/users.pkl")
cmdlnparser.add_argument('-s', '--sentimentpickle', help="pickle file containing dictionary mapping each product-user tuple to its sentiment score (input)", default="pkl/sentiments.pkl")
cmdlnparser.add_argument('-r', '--rounds', help="number of rounds to iterate for MCMC", default=100, type=int)
args = cmdlnparser.parse_args()
print("Command-line args:" + str(args.__dict__))
# defaults: args = argparse.ArgumentParser().parse_args(); args.productpickle = "products.pkl"; args.userpickle = "users.pkl"; args.sentimentpickle = "sentiments.pkl";

# Load products (R) and users (U)
with open(args.productpickle, 'rb') as f:
    R = pickle.load(f)
with open(args.userpickle, 'rb') as f:
    U = pickle.load(f)
with open(args.sentimentpickle, 'rb') as f:
    S = pickle.load(f)

# MCMC Sampling Algorithm
seed(3)
old_prob_R = {product: 0 for product in R}
prob_R = {product: 0.5 for product in R}
prob_U = {user: 0.5 for user in U}
k = 1
t1 = time.time()
while avg_of_abs_diffs(old_prob_R, prob_R) > 0.01: # terminate when average difference falls below 1%
    old_prob_R = deepcopy(prob_R)
    prob_R = draw_and_sample(R, prob_R, U, S, k, "R")
    prob_U = draw_and_sample(U, prob_U, R, S, k, "U")
    print("MCMC iteration", k, avg_of_abs_diffs(old_prob_R, prob_R))
    k += 1

print("Converged after", k, "iterations")
print("time Taken ", time.time() - t1)
# Store prob_R and prob_U in pickle files
product_probabilities_pkl = "pkl/product_probabilities.pkl"
with open(product_probabilities_pkl, 'wb') as f:
    pickle.dump(prob_R, f)
user_probabilities_pkl = "pkl/user_probabilities.pkl"   # currently not being used anywhere
with open(user_probabilities_pkl, 'wb') as f:
    pickle.dump(prob_U, f)
print("Parsed review data stored in " + product_probabilities_pkl + " and " + user_probabilities_pkl)