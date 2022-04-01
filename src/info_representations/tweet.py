from datetime import datetime
from nltk import tokenize, corpus
import re
from cleantext import clean

class Tweet:
    # TODO: use __slots__ to decrease memory usage 

    def __init__(self, id, datestring, text):
        self.id = id
        self.datetime = datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S")
        self.text = self._preprocess_text(text)

    def _preprocess_text(self, text):
        text = re.sub(r'pic.twitter.com/\S+',"", text)
        text = clean(text,
            fix_unicode=True,               
            to_ascii=True,              
            lower=True,                    
            no_line_breaks=False,  
            no_emoji=True,    
            no_urls=True,            
            no_emails=True,            
            no_phone_numbers=True,       
            no_numbers=False,             
            no_digits=False,             
            no_currency_symbols=True,    
            no_punct=True,
            replace_with_url="",
            replace_with_email="",
            replace_with_phone_number="",
            replace_with_number="",
            replace_with_punct="",        
        )

        words = tokenize.word_tokenize(text)

        cleaned_words = []
        for w in words:
            if w not in corpus.stopwords.words("english"):
                cleaned_words.append(w)
  
        return cleaned_words