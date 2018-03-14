from textblob import TextBlob

class ReviewTuple:
    def __init__(self, review):
        self.product = review["asin"]
        self.user = review["reviewerID"]
        self.sentiment = self.text2sentiment(review["reviewText"])

    def text2sentiment(self, text):
        return TextBlob(text).sentiment.polarity

    def __str__(self):
        return str(self.__dict__)