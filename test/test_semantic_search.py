### pytest unit tests ###

# Tests that no query is run if incorrect API key passed in
def test_incorrect_api_key():
    pass

# Tests that query is run if correct API key passed in
def test_correct_api_key():
    pass

# Tests that algorithm returns correct fields in json output
def test_json_format():
    # stub out bigquery function call
    pass

# Tests for correct error handling on timeout
def test_timeout():
    # stub out and timeout on bigquery function call
    pass

# Tests that hardcoded small dataset returns expected ranking
def test_size_10_ranking_order():
    pass

# Tests that hardcoded medium dataset returns expected ranking
def test_size_100_ranking_order():
    pass

# Tests that runtime does not exceed reasonable threshold
def test_runtime_size_100k_dataset():
    pass

# Tests that some results are returned when query doesn't exist in dataset
def test_query_not_in_dataset():
    pass
