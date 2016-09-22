from google.appengine.ext import ndb

class Password(ndb.Model):
    """ Holds a Password for this user. """
    
    service = ndb.StringProperty(default="")
    username = ndb.TextProperty()
    password = ndb.TextProperty()
    
    