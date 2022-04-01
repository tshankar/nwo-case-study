import json
import os
from google.cloud import bigquery
from datetime import datetime

from .info_representations.tweet import Tweet

# Defines API wrapper class for the semantic search algorithm
class SemanticSearchApi():
    def __init__(self, api_key_file):
        self.client = self._initialize_client(api_key_file)
        self.bq_tweet_table = 'nwo-sample.graph.tweets'
        self.table_sample_prob = 1e-6 
        self.rand_sample_prob = 0.01
        
        self.tweet_dict = {}
        self.top_k = 10

    def _initialize_client(self, api_key_file):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']=api_key_file
        return bigquery.Client()

    def get_trends(self, query):
        now = datetime.now() # TODO: confirm whether this is UTC time or not

        def recency_weighted_score(tweet):
            seconds_passed = (now - tweet.datetime).total_seconds()
            weight = 1 / seconds_passed # not small enough to have floating point issues 
            for word in tweet.words:
                if word != query:
                    if word not in word_scores:
                        word_scores[word] = weight
                    else:
                        word_scores[word] += weight

        # populate dictionary of sampled tweets if does not exist
        if not self.tweet_dict:
            self._get_tweets(self.bq_tweet_table)

        query_count = 0
        # TODO: what if query does not exist in dict
        if query in self.tweet_dict:
            query_tweet_list = self.tweet_dict[query]

            # get tweet count of query word
            query_count = len(query_tweet_list)
            word_scores = {}

            # get recency weighted score of associated words
            for tweet in query_tweet_list:
                recency_weighted_score(tweet)                    

            # normalize by query count
            word_scores = {w: s / query_count for w, s in word_scores.items()}

            # sort by score and get top k words
            word_score_list = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
            top_k_word_scores = word_score_list[:self.top_k]

            # get json representation of words
            print(self._jsonify(query, top_k_word_scores))

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

            # count every word only once per tweet 
            tweet_words = {}
            for word in tweet.words:
                if word not in tweet_words:
                    tweet_words[word] = True

            # add words in tweet to dictionary
            for word in tweet_words:
                if word not in self.tweet_dict:
                    self.tweet_dict[word] = [tweet]
                else:
                    self.tweet_dict[word].append(tweet)
            i += 1
            if (i % 1000 == 0): print(i)

    # JSONifies ranked trends in results
    def _jsonify(self, query, word_scores):
        json_string = "{"
        json_string += "\"{}\": {{\n".format(query)
        json_string += "\"top_{}_words\": {{\n".format(self.top_k)
        for i in range(len(word_scores)):
            (word, _) = word_scores[i]
            json_string += "\"{}\": \"{}\"".format(i, word)
            if i < len(word_scores) - 1:
                json_string += ","
            json_string += "\n"
        json_string += "}\n}\n}"
        return json_string
        

    
