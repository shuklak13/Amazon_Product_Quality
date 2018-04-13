# Import and Initialize
import argparse, pickle
from random import seed, random
from auxiliary import prob, avg_of_abs_diffs
from copy import deepcopy    
import time
from collections import Counter
import sys
if sys.version_info > (3, 2):
    from functools import reduce

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
# Parameters determining the distribution P(R,U|S)
sigma = 0.1  # probabilities that a positive user rates a positive product negatively; "noise factor"
alpha = 0.3  # probabilities that a positive user rates a negative product positively
beta = 0.6  # probabilities that a negative user rates a positive product positively
p_S_1_given_R_U = {
    (0, 0): sigma ** 2,
    (0, 1): alpha,
    (1, 0): beta,
    (1, 1): 1 - sigma
}


def p_S_given_R_U(s, r, u):
    return p_S_1_given_R_U[(r, u)] if s else 1 - p_S_1_given_R_U[(r, u)]


# MCMC Sampling Algorithm
seed(3)
old_prob_R = {product: 0 for product in R}
prob_R = {product: 0.5 for product in R}
prob_U = {user: 0.5 for user in U}



def sentiment(listOfReviewTuples):   # A = list of review tuples
    sentimentList = [reviewTuple.sentiment for reviewTuple in listOfReviewTuples]
    return Counter(sentimentList).most_common(1)[0][0]

def draw(predicting, i):

    if predicting == "R":
        sumPos = reduce(lambda x, y: x * y, [p_S_given_R_U(S[(k, i)], 1, sentiment(U[k])) for k in U.keys() if (k, i) in S])
        sumNeg = reduce(lambda x, y: x * y, [p_S_given_R_U(S[(k, i)], 0, sentiment(U[k])) for k in U.keys() if (k, i) in S])
    else:
        sumPos = reduce(lambda x, y: x * y, [p_S_given_R_U(S[(i, k)], sentiment(R[k]), 1) for k in R.keys() if (i, k) in S])
        sumNeg = reduce(lambda x, y: x * y, [p_S_given_R_U(S[(i, k)], sentiment(R[k]), 0) for k in R.keys() if (i, k) in S])

    def probability_clause():
        return sumPos if sentiment(A[i]) else sumNeg
        # return prob_A[i] * (
        #     p_S_given_R_U[1, 0] * p_S_given_R_U[1, 1] if predicting == "R"
        #     else p_S_given_R_U[0, 1] * p_S_given_R_U[1, 1]
        # )

    def partition_function():
        # return sum([probability_clause(i) for i in A])
        # return prob_A[i] * p_S_given_R_U[1, 0] * p_S_given_R_U[1, 1] +
        #    prob_A[i] p_S_given_R_U[0, 1] * p_S_given_R_U[1, 1]
        # if predicting == "R":
        #     return reduce(lambda x, y: x*y, [p_S_given_R_U(S[(U[k], 1)], 1, U[k]) for k = U.keys()], 1) + 
        #     reduce(lambda x, y: x*y, [p_S_given_R_U(S[(U[k], 0)], 0, U[k]) for k = U.keys()], 1)
        # else:
        #     return reduce(lambda x, y: x*y, [p_S_given_R_U(S[(1, R[k])], R[k], 1) for k = R.keys()], 1) + 
        #     reduce(lambda x, y: x*y, [p_S_given_R_U(S[(0, R[k])], R[k], 0) for k = R.keys()], 1)
        return sumPos + sumNeg
    
    A = R
    prob_A = prob_R
    B = U
    prob_B = prob_U
    if predicting == "U":
        prob_A = prob_U
        A = U
        prob_B = prob_R
        B = R
    
    p = probability_clause() / partition_function()
    return random() < p


def draw_and_sample(A, k, prob_A, predicting="R"):

    for i in A:
        sample_A_i = draw(predicting, i)  # draw sample
        prob_A_i = prob(prob_A[i], sample_A_i)  # probability of drawing that sample
        A_i_k = prob_A_i >= random()  # rejection sampling
        prob_A[i] = (k * prob_A[i] + A_i_k) / (k + 1)  # update probability based on sample

    return prob_A

def MCMCAlgo():
    t1 = time.time()
    k = 1
    global old_prob_R
    global prob_R
    global prob_U
    
    i = 0
    while i < 10:
        old_prob_R = deepcopy(prob_R)
        prob_R = draw_and_sample(R, k, prob_R, "R")
        prob_U = draw_and_sample(U, k, prob_U, "U")
        print("MCMC iteration", k, avg_of_abs_diffs(old_prob_R, prob_R))
        k += 1
        i = i+1
    print("Converged after", k, "iterations")
    print("time Taken ", time.time() - t1)

    
def storeResults():
    # Store prob_R and prob_U in pickle files
    product_probabilities_pkl = "pkl/product_probabilities.pkl"
    with open(product_probabilities_pkl, 'wb') as f:
        pickle.dump(prob_R, f)
    user_probabilities_pkl = "pkl/user_probabilities.pkl"  # currently not being used anywhere
    with open(user_probabilities_pkl, 'wb') as f:
        pickle.dump(prob_U, f)
    print("Parsed review data stored in " + product_probabilities_pkl + " and " + user_probabilities_pkl)

if __name__ == "__main__":
    print("running MCMC")
    MCMCAlgo()
    print("storing results")
    storeResults()
    print("finished!")
