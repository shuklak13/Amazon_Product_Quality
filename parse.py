# Import and Initialize
import animation, pickle, argparse
from collections import defaultdict
products = defaultdict(list)
users = defaultdict(list)
sentiments = dict()

# Read-in Command-Line Arguments
cmdlnparser = argparse.ArgumentParser()
cmdlnparser.add_argument('-d', '--data', help="data file containing Amazon review data (input", default="data/reviews_Amazon_Instant_Video_5.json.gz")
cmdlnparser.add_argument('-p', '--productpickle', help="pickle file containing dictionary mapping each product to its reviews (output)", default="pkl/products.pkl")
cmdlnparser.add_argument('-u', '--userpickle', help="pickle file containing dictionary mapping each user to his or her reviews (output)", default="pkl/users.pkl")
cmdlnparser.add_argument('-s', '--sentimentpickle', help="pickle file containing dictionary mapping each user-product tuple to its sentiment score (output)", default="pkl/sentiments.pkl")
args = cmdlnparser.parse_args()
print("Command-line args:" + str(args.__dict__))

# Function for parsing json.gz files
def parse(path):
    import gzip
    from ReviewTuple import ReviewTuple
    g = gzip.open(path, 'r')
    for l in g:
        yield ReviewTuple(eval(l))

# Parse json.gz file into "products" and "users" dictionaries
print("Parsing review data from " + args.data + "... \nThis might take a minute...")
animation.start()
for review in parse(args.data):
    products[review.product].append(review)
    users[review.user].append(review)
    sentiments[(review.user, review.product)] = review.sentiment

# Store "products" and "users" in pickle files
with open(args.productpickle, 'wb') as f:
    pickle.dump(products, f)
with open(args.userpickle, 'wb') as f:
    pickle.dump(users, f)
with open(args.sentimentpickle, 'wb') as f:
    pickle.dump(sentiments, f)
animation.end()
print("Parsed review data stored in " + args.productpickle + ", " + args.userpickle + ", and " + args.sentimentpickle)