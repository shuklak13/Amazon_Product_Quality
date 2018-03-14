data_path = "reviews_Amazon_Instant_Video_5.json.gz"
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
print("Parsing review data... may take a minute...")
animation.start()
for review in parse(data_path):
    products[review.product].append(review)
    users[review.user].append(review)

import pickle
with open("products.pkl", 'wb') as f:
    pickle.dump(products, f)
animation.end()