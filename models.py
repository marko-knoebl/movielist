from google.appengine.ext import ndb

class Movie(ndb.Model):
    # data model for a movie:
    #    contains the movie title, a rating from 1-5
    #    and a URL to an image
    name = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    image = ndb.StringProperty()
