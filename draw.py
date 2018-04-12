from random import random
from auxiliary import prob, multiply

# Parameters determining the distribution P(R,U|S)
sigma = 0.1 #probabilities that a positive user rates a positive product negatively; "noise factor"
alpha = 0.3 #probabilities that a positive user rates a negative product positively
beta  = 0.6 #probabilities that a negative user rates a positive product positively
p_S_given_R_U = {
    (0,0): sigma**2,
    (0,1): alpha,
    (1,0): beta,
    (1,1): 1-sigma
}

# Sample from P(A_i | A_(-i), B, S)
def draw(A, i, prob_A, B, S, predicting="R"):
    def probability_clause(i):
        return prob_A[i] * (
            p_S_given_R_U[1,0] * p_S_given_R_U[1,1] if predicting=="R"
            else p_S_given_R_U[0,1] * p_S_given_R_U[1,1]
        )
                            # multiply(
                            #     [prob(p_S_given_R_U[1, j], S[i, j]) for j in B]
                            # )

    def partition_function():
        return sum([probability_clause(i) for i in A])

    p = probability_clause(i) / partition_function()
    return random() < p

# For every feature i in A, draw from P(A_i | A_(-i), B, S) and update P(A)
def draw_and_sample(A, prob_A, B, S, k, predicting="R"):
    for i in A:
        sample_A_i  = draw(A, i, prob_A, B, S, predicting)      # draw sample
        prob_A_i    = prob(prob_A[i], sample_A_i)   # probability of drawing that sample
        A_i_k       = prob_A_i >= random()          # rejection sampling
        prob_A[i]   = (k*prob_A[i] + A_i_k)/(k+1)   # update probability based on sample
    return prob_A