class BotListener(tweepy.StreamingClient):

    api = tweepy.Client(consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True)

    # def on_data(self, raw_data):
    #     print(raw_data.user)

    # def on_tweet(self, tweet):
    #     try:
    #         split1,split2 = tweet.text.lower().split('question:') # splits string from specified delimiter 'question:'

    #         returned_query = queries.Query().search(split2)

    #         print("ONE")

    #         if returned_query==None:
    #             ''' triggered if returned_query return None '''
    #             raise Exception()

    #         print("TWO")


    #         time.sleep(0.5)

    #         Tweeter.tweet(f'Hey, you want to fact check: {split}\n\n Answer: {returned_query.results_text.snippet} \n Link:{returned_query.results_text.link} ')

    #         print("THREE")

    #         time.sleep(0.5)

    #     except e:
    #         ''' triggered when try block error is triggered '''
    #         print(e)      
    # 
    def on_tweet(self, tweet):
        print(tweet)

bot = BotListener(bearer_token="AAAAAAAAAAAAAAAAAAAAABV%2BlQEAAAAA%2FlKzfXimuHhAC5%2Bdt6GlmougAoA%3DPH2bZtRqIJgPbJ8QlX6BwBB6w7jfOYPYD6klMPVI3sdAww7L9W")
bot.add_rules(tweepy.StreamRule("@heyHelpMe0ut 'question:'")) # rule which is triggered when user tweets with @ and tweet contains question
bot.add_rules(tweepy.StreamRule("@heyHelpMe0ut 'is:reply'")) # rule which is triggered when user qoute tweets a tweet with @
bot.filter()