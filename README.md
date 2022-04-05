# nwo-case-study
This is an implementation of a semantic search algorithm. 

## API
Given a query word, the algorithm returns a list of the top k most related words.

For example, given query input `biden`, the response might be:
```
{
	"biden": {
		"top_10_words": [
			"joe",
			"trump",
			"dont",
			"bidens",
			"time",
			"like",
			"coronavirus",
			"blah",
			"dems",
			"obama"
		]
	}
}
```
## Algorithm
The current implementation takes inspiration from association rule mining and uses Twitter data to determine the association of the word `w` with the query word `q`

Specifically, the association of `w` and `q` can be measured by two metrics: 
1) The frequency with which both words co-occurred in tweets
2) The recency of the tweets in which they co-occurred

Let T represent the set of tweets in which `w` and `q` co-occur. To calculate the association score of `w` with `q`, we weight every co-occurrence of `w` and `q` with a recency score and normalize it by the number of occurrences of `q`: 

<img src="https://latex.codecogs.com/svg.image?score(w,q)&space;=&space;\frac{\sum_{w&space;\in&space;T}weight(w)}{count(q)}">


Each word `w` scored is only counted once per tweet, and only if it is not the query word. 

Instead of querying BigQuery directly for each input word, ~70k tweets are sampled randomly from the BigQuery table upon the first query and are cached for following queries. 

## Setup
### Dependencies
- python 3.8
- google-cloud-bigquery 3.0.1
- nltk 3.7
- clean-text 0.6.0

## Execution
- Modify the path to the BigQuery API key in `./main.py` with your own
- Run `python main.py`

