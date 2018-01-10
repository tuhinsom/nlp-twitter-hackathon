import re
from nltk.corpus import stopwords
from collections import Counter
import string

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

class analysis_utilities(object):


	def __init__(self):
		self = self

	def tokenize(self, s):
		return tokens_re.findall(s)

	def preprocess(self, s, lowercase=False):
		tokens = self.tokenize(s)
		if lowercase:
			tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]

		return tokens


	def eliminate_stopwords(self, tokens):


		punctuation = list(string.punctuation)
		stop = stopwords.words('english') + punctuation + ['rt', 'via']
		tokens = [term for term in tokens if term not in stop]

		return tokens

	def feed_text_counts(self, tokens):
		count_all = Counter()
		count_all.update(tokens)
		most_common = count_all.most_common(5)
		# Count terms only once, equivalent to Document Frequency
		#terms_single = set(tokens)
		# Count hashtags only
		terms_hash = [term for term in tokens if term.startswith('#')]
		terms_mentions = [term for term in tokens if term.startswith('@')]
		# Count terms only (no hashtags, no mentions)
		#terms_only = [term for term in tokens if term not term.startswith(('#', '@'))]

		return { "most_common": most_common, "terms_hash":terms_hash,"terms_mentions":terms_mentions}
