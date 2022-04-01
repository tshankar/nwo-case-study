import json
import os
from google.cloud import bigquery

from .info_representations.tweet import Tweet

# Defines API wrapper class for the semantic search algorithm
class SemanticSearchApi():
    def __init__(self, api_key_file):
        self.client = self._initialize_client(api_key_file)
        self.bq_tweet_table = 'nwo-sample.graph.tweets'
        self.sample_prob = 0.0000001
        
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
            """.format(bq_table, self.sample_prob)
        query_job = self.client.query(query_string)
        results = query_job.result() 

        # create Tweets and populate the tweet table
        for row in results:
            tweet = Tweet(row.tweet_id, row.created_at, row.tweet)
        
        # populate tweet table here

    # JSONifies ranked trends in results
    def _jsonify(self, results):
        pass
    
