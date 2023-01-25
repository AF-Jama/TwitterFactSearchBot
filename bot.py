import tweepy
from dotenv import load_dotenv
from Queries import Query
import time
import os

load_dotenv()

API_KEYS = os.getenv('API_KEYS')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
BEARER_TOKEN =  os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
      
# api = tweepy.Client(consumer_key=API_KEYS,
# consumer_secret=API_KEY_SECRET,
# access_token=ACCESS_TOKEN,
# access_token_secret=ACCESS_TOKEN_SECRET,
# wait_on_rate_limit=True)

class Tweeter:
    WAIT_ON_LIMIT=True

    def __init__(self,consumer_key,consumer_secret,access_token,access_token_secret):
        # creating private instance attributes
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret
        self.API = tweepy.Client(consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True)



    
    def tweet(self,status,in_reply_to_id = None):
        ''' class method takes string and tweet id which refers to initial tweet '''
        self.API.create_tweet(text=status,in_reply_to_tweet_id= in_reply_to_id,)

    def return_tweet_from_id(self,id):
        response = self.API.get_tweet(id=id,tweet_fields=["text"],user_auth=True) # returns response
        if(response.data is None):
            ''' triggered if data response attriute is None meaning tweet id does not map to a tweet ie: invalid id '''
            return None

        print(response.data)

        return response.data.text.strip() # returns text attribute and strips unnessecary whitespace

    @classmethod
    def home(cls):
      public_tweets = cls.api.home_timeline()
      for tweet in public_tweets:
         print(tweet.text)

    @classmethod
    def wait_on_limit_status(cls):
        return cls.WAIT_ON_LIMIT



class Listener(tweepy.StreamingClient):   
    # stream_rules = [tweepy.StreamRule("@heyHelpMe0ut 'question:'"),tweepy.StreamRule("@heyHelpMe0ut 'is:reply'")]
    stream_rules = [tweepy.StreamRule('"@heyHelpMe0ut" "-q"'),tweepy.StreamRule('"@heyHelpMe0ut" is:reply')]

    def __init__(self, bearer_token,consumer_key,consumer_secret,access_token,access_token_secret):
        super().__init__(bearer_token)
        self.tweet = Tweeter(consumer_key, consumer_secret, access_token, access_token_secret)

    def on_tweet(self, tweet):
        ''' Tweets that are triggered on this method are either direct @ with a question:, or a reply to a tweet which references a tweet above it that must be parsed and fact checked '''
        if(tweet.referenced_tweets is not None):
            ''' triggered if referenced tweets does not evaluate to None and represents a reply or qoute to a tweet '''
            referenced_tweet_id = tweet.referenced_tweets[0].id # returns referenced tweet id 
            print(referenced_tweet_id)
            try:
                referenced_tweet_content = self.tweet.return_tweet_from_id(referenced_tweet_id)
                print(referenced_tweet_content)
                if referenced_tweet_content is None:
                    raise Exception("Content has no content, id may be not map to a tweet")

                # self.tweet.tweet(referenced_tweet_content)
                query_response = Query.search(referenced_tweet_content)

                if query_response is None:
                    raise Exception("Query response is None")

                tweet_response = f'Hey we have crawled the web and the following has been found on this:\n\nResponse: {query_response["results_text"]["snippet"]}\n\nLink: {query_response["results_text"]["link"]}'

                # time.sleep(2)

                print(tweet_response)

                self.tweet.tweet(tweet_response,in_reply_to_id=tweet.id)




            except:
                print("expeption")

            

        elif(tweet.referenced_tweets is None):
            print("HERE")
            ''' triggered if referenced tweets evaluate to None and represent a standard tweet '''
            try:
                print(tweet.text)
                tweet_string = tweet.text.lower()
                split1,split2 = tweet_string.split("-q")
                print(split2)
                if not split2.strip():
                    ''' triggered if normalised text query is empty '''
                    raise Exception("Query is empty")

                else:
                    query_response = Query.search(split2)


                    tweet_response = f'Hey we have crawled the web and the following has been found on this:\n\nResponse: {query_response["results_text"]["snippet"]}\n\nLink: {query_response["results_text"]["link"]}'

                    # time.sleep(2)

                    print(tweet_response)

                    self.tweet.tweet(tweet_response,in_reply_to_id=tweet.id)


            except:
                print("Tweet exception")


    def on_connect(self):
        print("SUCCESFUL CONNECTION")

    def on_connection_error(self):
        self.run()

    def on_disconnect(self):
        self.run()
    

    def run(self):
        self.add_rules(add=self.stream_rules)
        self.filter(threaded=True,expansions="author_id",tweet_fields=["created_at","conversation_id","in_reply_to_user_id","referenced_tweets","entities"])



# l = Listener(bearer_token=BEARER_TOKEN,consumer_key=API_KEYS,consumer_secret=API_KEY_SECRET,access_token=ACCESS_TOKEN,access_token_secret=ACCESS_TOKEN_SECRET)
# l.run()

# print(API_KEYS)
# print(API_KEY_SECRET)
# print(ACCESS_TOKEN)
# print(ACCESS_TOKEN_SECRET)

api = tweepy.Client(consumer_key=API_KEYS,
consumer_secret=API_KEY_SECRET,
access_token=ACCESS_TOKEN,
access_token_secret=ACCESS_TOKEN_SECRET,
wait_on_rate_limit=True)

# print(api.get_tweet(id=1613938177676574721,tweet_fields=['text'],user_auth=True).data.text.strip())


# print(Tweeter(API_KEYS, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET).return_tweet_from_id(1616465599361683456))

if __name__ == "__main__":
    l = Listener(bearer_token=BEARER_TOKEN,consumer_key=API_KEYS,consumer_secret=API_KEY_SECRET,access_token=ACCESS_TOKEN,access_token_secret=ACCESS_TOKEN_SECRET)
    l.run()