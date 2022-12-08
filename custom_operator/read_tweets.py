from airflow.models import BaseOperator
# Importing the libraries
import configparser
import tweepy
import pandas as pd


class ReadHashtagTweet(BaseOperator):

    TODO: """Accept Hashtag, Get Date, Get Limits, Get Location of file, Get column names"""

    def __init__(self,
                hashtag,
                date_since,
                limits,
                file_name,
                column_names,
                *args,
                **kwargs):
        self.hashtag = hashtag
        self.date_since = date_since
        self.limits = limits
        self.file_name = file_name
        self.column_names = column_names
        super().__init__(*args,**kwargs)


    def execute(self, context):

            # Read twitter api Configuration
            config_location = '/opt/airflow/dags/custom_operator/config.ini'
            config = configparser.ConfigParser()
            config.read(config_location)

            api_key = config['twitter']['api_key']
            api_key_secret = config['twitter']['api_key_secret']
            access_token = config['twitter']['access_token']
            access_token_secret = config['twitter']['access_token_secret']

            print(api_key_secret)

            # Authenticate
            auth = tweepy.OAuthHandler(api_key, api_key_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)

            hashtag = self.hashtag
            limits=self.limits
            date_since = self.date_since
            search = hashtag + date_since
            columns = self.column_names
            data = []
            tweets = tweepy.Cursor(api.search_tweets, q=hashtag,
                                          lang="en", 
                                          tweet_mode='extended').items(self.limits)

            for tweet in tweets:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

            df = pd.DataFrame(data, columns=columns)

            print(df)
            df.to_csv(self.file_name, sep='\t', encoding='utf-8')