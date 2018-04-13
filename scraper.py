from lxml import html
import csv,os,json
import requests
from time import sleep

def parse(asin):
    url = "http://www.amazon.com/dp/"+asin
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    doc = html.fromstring(page.content)           
    XPATH_REVIEW = '//span[@class="reviewCountTextLinkedHistogram noUnderline"]//text()'
    # print("doc: " + doc)
    # print("RAW_REVIEW: " + RAW_REVIEW)
    RAW_REVIEW = doc.xpath(XPATH_REVIEW)            
    if RAW_REVIEW is None:
        return None
    else:
        REVIEW = ' '.join(RAW_REVIEW).strip()
        RATING = REVIEW.split(' ')[0]
        return RATING

if __name__ == "__main__":
    import pickle
    with open("pkl/product_probabilities.pkl", 'rb') as f:
        probabilities = pickle.load(f)
    ratings = {}
    ctr = 0
    for asin in probabilities:
        ctr += 1
        rating = parse(asin.strip())
        if rating:
            ratings[asin] = rating
        print(asin, "\t", ctr, "/", len(probabilities), rating, probabilities[asin])
    amzn_ratings_pkl = "pkl/amzn_ratings.pkl"
    with open(amzn_ratings_pkl, 'wb') as f:
        pickle.dump(ratings, f)
        