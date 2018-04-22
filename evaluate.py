from numpy import array, corrcoef
from scipy.stats import linregress
import pickle
import numpy as np
import matplotlib.pyplot as plt

with open("pkl/product_probabilities.pkl", 'rb') as f:
    probabilities = pickle.load(f)

with open("pkl/amzn_ratings.pkl", 'rb') as f:
    ratings = pickle.load(f)

ratings = {product: ratings[product] for product in ratings if ratings[product] is not ''}

product_probability_rating = []
for product in ratings:
    product_probability_rating.append((product, 4.0*probabilities[product] +1, ratings[product]))
x = array([float(ppr[1]) for ppr in product_probability_rating])
y = array([float(ppr[2]) for ppr in product_probability_rating])
print(linregress(x,y))

# Correlations
print ("Correlation", corrcoef(x,y))

# Scatter Plots 
plt.scatter(x,y)
plt.xlabel("Predicted Rating")
plt.ylabel("Actual Rating")
plt.title("Scatter Plot between Predicted and Actual Rating")
plt.show()