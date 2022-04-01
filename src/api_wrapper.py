import json
import os
from google.cloud import bigquery

from .info_representations.tweet import Tweet

# Defines API wrapper class for the semantic search algorithm
class SemanticSearchApi():
    def __init__(self, api_key_file):
        self.client = self._initialize_client(api_key_file)
        self.bq_tweet_table = 'nwo-sample.graph.tweets'
        self.table_sample_prob = 1e-8 # returns about 1 million rows
        self.rand_sample_prob = 0.001
        
        self.tweet_dict = {}

        pass

    def _initialize_client(self, api_key_file):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']=api_key_file
        return bigquery.Client()

    # Performs 
    def get_trends(self, query):
        # populate dictionary of sampled tweets if does not exist
        if not self.tweet_dict:
            self._get_tweets(self.bq_tweet_table)
        
        # calculate the confidence in related words
        

    # TODO: check for correct API key and throw error if not
    def _get_tweets(self, bq_table):
        query_string = \
            """
            SELECT *
            FROM {}
            TABLESAMPLE SYSTEM({} PERCENT)
            WHERE RAND() < {}
            """.format(bq_table, self.table_sample_prob, self.rand_sample_prob)
        query_job = self.client.query(query_string)
        results = query_job.result() 

        # create Tweets and populate the tweet table
        i = 0
        for row in results:
            tweet = Tweet(row.tweet_id, row.created_at, row.tweet)

            # don't count any word more than once
            tweet_words = {}
            for word in tweet.text:
                if word not in tweet_words:
                    tweet_words[word] = True

            # add words in tweet to dictionary
            for word in tweet_words:
                if word not in self.tweet_dict:
                    self.tweet_dict[word] = [tweet]
                else:
                    self.tweet_dict[word].append(tweet)
            i += 1
            print(i)

        # populate tweet table here
        print(self.tweet_dict["america"])

    # JSONifies ranked trends in results
    def _jsonify(self, results):
        pass
    
