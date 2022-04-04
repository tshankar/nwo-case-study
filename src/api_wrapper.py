from datetime import datetime
from google.cloud import bigquery
import os
import sys


from .info_representations.tweet import Tweet

### API wrapper for the semantic search algorithm ###
class SemanticSearchApi():
    def __init__(self, api_key_file):
        self.client = self._initialize_client(api_key_file)
        self.bq_tweet_table = 'nwo-sample.graph.tweets'
        self.table_sample_prob = 1e-6 
        self.rand_sample_prob = 0.05
        
        self.tweet_dict = {}
        self.top_k = 10

    """ Initializes BigQuery client with provided API key """
    def _initialize_client(self, api_key_file):
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS']=api_key_file
            return bigquery.Client()
        except:
            print("Error: Cannot initialize BigQuery client. Please check provided credentials.")
            sys.exit(1)

    """ Retrieves top k trending words associated with the provided query word """
    def get_trends(self, query):
        now = datetime.now() 

        # computes score of each word in the provided tweet based on recency 
        def score(tweet):
            seconds_passed = (now - tweet.datetime).total_seconds()
            weight = 1 / seconds_passed 
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
        top_k_word_scores = []
        if query in self.tweet_dict:
            query_tweet_list = self.tweet_dict[query]

            # get tweet count of query word
            query_count = len(query_tweet_list)
            word_scores = {}

            # get recency weighted score of associated words
            for tweet in query_tweet_list:
                score(tweet)                    

            # normalize by query count
            word_scores = {w: s / query_count for w, s in word_scores.items()}

            # sort by score and get top k words
            word_score_list = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
            top_k_word_scores = word_score_list[:self.top_k]
                    
        # get json representation of words
        return self._jsonify(query, top_k_word_scores)

    """ Performs query to retrieve tweets from BigQuery """
    def _get_tweets(self, bq_table):
        try:
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
                if (i % 1000 == 0): 
                    print("Retrieved {} tweets".format(i))
        except: 
            print("Error: Could not retrieve data from BigQuery table: {}".format(bq_table))

    """Creates JSON object mapping query to the top_k associated words """
    def _jsonify(self, query, word_scores):
        def indent(n):
            return n * "\t"

        json_string = "{\n"
        json_string += "{}\"{}\": {{\n".format(indent(1), query)
        json_string += "{}\"top_{}_words\": [\n".format(indent(2), self.top_k)
        for i in range(len(word_scores)):
            (word, _) = word_scores[i]
            json_string += "{}\"{}\"".format(indent(3), word)
            if i < len(word_scores) - 1:
                json_string += ","
            json_string += "\n"
        json_string += "{}]\n".format(indent(2))
        json_string += "{}}}\n}}".format(indent(1))
        return json_string
    
        

    
