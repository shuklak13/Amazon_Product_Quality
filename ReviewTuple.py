from textblob import TextBlob

class ReviewTuple:
    def __init__(self, review):
        self.product = review["asin"]
        self.user = review["reviewerID"]
        self.sentiment = text2sentiment(review["reviewText"])

    def __str__(self):
        return str(self.__dict__)


def text2sentiment(text):
    return (TextBlob(text).sentiment.polarity>0)