# Import and Initialize
import argparse, pickle
from random import seed, random
from draw import draw_and_sample
from auxiliary import prob

# Read-in Command-Line Arguments
cmdlnparser = argparse.ArgumentParser()
cmdlnparser.add_argument('-p', '--productpickle', help="pickle file containing dictionary mapping each product to its reviews (input)", default="products.pkl")
cmdlnparser.add_argument('-u', '--userpickle', help="pickle file containing dictionary mapping each user to his or her reviews (input)", default="users.pkl")
cmdlnparser.add_argument('-s', '--sentimentpickle', help="pickle file containing dictionary mapping each product-user tuple to its sentiment score (input)", default="sentiments.pkl")
cmdlnparser.add_argument('-r', '--rounds', help="number of rounds to iterate for MCMC", default=10, type=int)
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
prob_R = {product: 0.5 for product in R}
prob_U = {user: 0.5 for user in U}
for k in range(1, args.rounds):
    prob_R = draw_and_sample(R, prob_R, U, S, k, "R")
    prob_U = draw_and_sample(U, prob_U, R, S, k, "U")

# Store prob_R and prob_U in pickle files
product_probabilities_pkl = "product_probabilities.pkl"
with open(product_probabilities_pkl, 'wb') as f:
    pickle.dump(prob_R, f)
user_probabilities_pkl = "user_probabilities.pkl"
with open(user_probabilities_pkl, 'wb') as f:
    pickle.dump(prob_U, f)
print("Parsed review data stored in " + product_probabilities_pkl + " and " + user_probabilities_pkl)