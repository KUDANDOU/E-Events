from twitter import *
# import settings
# import tweepy
# import dataset
# from textblob import TextBlob
# from sqlalchemy.exc import ProgrammingError
# import json
# from stuf import stuf

# db = dataset.connect('sqlite:///tweets.db',row_type=stuf)

consumer_key = 'AROGxAliStQtIzYTpTcpNp8Ga'
consumer_secret = 'tBgnvA9mdqXyZxP6f4i6HQrcOZVjSgycE2L4HqpzMnQEbg0Kyr'
access_key = '842347271370997761-M1mbOB9ptLd5t1dPUr5Y7QCyLl0DSkj'
access_secret ='m8ELeOAanfLsOmfqJ3GUVMEbbhU1cIol4j5MH9CbgHg1A'


#result = db["tweets"].all()
#print (result)
# for user in db['tweets']:
#     print(user['name'])

t = Twitter(
     auth=OAuth(access_key, access_secret, consumer_key, consumer_secret))


t.direct_messages.new(
    user="mallan04",
    text="hie mandla")

    
    