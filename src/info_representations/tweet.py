from datetime import datetime
import nltk
from string import punctuation
import re

class Tweet:
    # TODO: use __slots__ to decrease memory usage 

    def __init__(self, id, datestring, text):
        self.id = id
        self.datetime = datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S")
        self.text = self._preprocess_text(text)

    # TODO: make this more efficient 
    def _preprocess_text(self, text):
        # remove punctuation
        def remove_punctuation(s):
            all_punctuation = punctuation + [u'\u201c',u'\u201d',u'\u2018',u'\u2019']
            return ''.join(c for c in s if c not in all_punctuation) 

        # make lowercase letters
        def to_lower(s):
            return ''.join([c.lower() for c in s])

        # remove hyperlinks
        def remove_links(s):
            # TODO: remove links to pictures
            s = re.sub(r"http\S+", "", s)
            s = re.sub(r'pic.twitter.com/\S+',"", s)
            return s

        text = remove_links(text)
        text = to_lower(remove_punctuation(text))
        words = nltk.tokenize.word_tokenize(text)
        print(words)

        # make lowercase letters

        # remove links

        return []