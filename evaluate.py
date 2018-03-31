import pickle
with open("pkl/product_probabilities.pkl", 'rb') as f:
    probabilities = pickle.load(f)

ratings = {
    "B006Y5BWQG": 4.7,
    "B007943UZ2": 3.8,
    "B00EDG3GQ2": 4.5,
    "B009IF7092": 4.8,
    "B00HBJ9XGU": 4.5,
    "B00BG69SEQ": 4.5,
    "B00KD9N9BA": 4.3,
    "B00AEFVNFC": 3.5,
    "B002OLLH46": 3.1,
    "B001F6ZIXC": 4.7,
    "B00978LMCG": 2.4,
    "B003UU1UTC": 4.4,
    "B008XFAZRW": 4.5,
    "B00IAKMVHM": 3.7,
    "B00DMLRI0O": 2.4,
    "B003FGKBSC": 4.7,
    "B008JSNIQS": 4.6,
    "B009M9GI06": 3.1,
    "B007WPLZAK": 4.1,
    "B00EY7YGBO": 4.7
}

from numpy import array
from scipy.stats import linregress
product_probability_rating = []
for product in ratings:
    product_probability_rating.append((product, probabilities[product], ratings[product]))
x = array([ppr[1] for ppr in product_probability_rating])
y = array([ppr[2] for ppr in product_probability_rating])
print(linregress(x,y))