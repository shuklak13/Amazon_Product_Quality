import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', help="data file containing Amazon review data (input of parse.py", default="reviews_Amazon_Instant_Video_5.json.gz")
parser.add_argument('-p', '--pickle', help="pickle file containing parsed review data (output of parse.py)", default="products.pkl")
args = parser.parse_args()
print("Command-line args:" + str(args.__dict__))

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
print("Parsing review data from " + args.data + "... \nThis might take a minute...")
animation.start()
for review in parse(args.data):
    products[review.product].append(review)
    users[review.user].append(review)

import pickle
with open(args.pickle, 'wb') as f:
    pickle.dump(products, f)
animation.end()
print("Parsed review data stored in " + args.pickle)