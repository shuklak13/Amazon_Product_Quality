import sys
data_path = sys.argv[1] if len(sys.argv)>1  else "reviews_Amazon_Instant_Video_5.json.gz"
pkl_path  = sys.argv[2] if len(sys.argv)>2  else "products.pkl"

def parse(path):
    from ReviewTuple import ReviewTuple
    import gzip
    g = gzip.open(path, 'r')
    for l in g:
        yield ReviewTuple(eval(l))

from collections import defaultdict
products = defaultdict(list)
users = defaultdict(list)

import animation
print("Parsing review data from " + data_path + "... \nThis might take a minute...")
animation.start()
for review in parse(data_path):
    products[review.product].append(review)
    users[review.user].append(review)

import pickle
with open(pkl_path, 'wb') as f:
    pickle.dump(products, f)
animation.end()
print("Parsed review data stored in " + pkl_path)