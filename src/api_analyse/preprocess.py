import re
import string
import json
import os
from typing import List, Optional

try:
    # Import NLTK components if available; otherwise use simple fallback
    from nltk.stem import WordNetLemmatizer
    from nltk.stem import PorterStemmer
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
except Exception:
    lemmatizer = None
    stemmer = None


def preprocess_text(tweet: str, stem_or_lem: str = "lem", emojis: Optional[dict] = None, stopwords_list: Optional[List[str]] = None) -> str:
    """Preprocess a tweet-like text for the sentiment model.

    Steps:
    - Remove URLs, mentions and hash signs
    - Replace emojis via provided dict
    - Remove non-ascii characters
    - Lowercase, remove punctuation
    - Tokenize, remove stopwords
    - Lemmatize or stem when NLTK is available
    """

    if not isinstance(tweet, str):
        return ""

    # 1. Basic cleaning
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r"@\w+", '', tweet)
    tweet = re.sub(r"#", '', tweet)

    # 2. Emoji replacement
    if emojis:
        for emo, desc in emojis.items():
            tweet = tweet.replace(emo, f" {desc} ")

    # 3. Remove non-ASCII
    tweet = re.sub(r'[^\x00-\x7F]+', '', tweet)

    # 4. Lowercase and remove punctuation
    tweet = tweet.lower()
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))

    # 5. Tokenize
    tokens = tweet.split()

    # 6. Stopwords
    if stopwords_list:
        tokens = [w for w in tokens if w not in stopwords_list]

    # 7. Lemmatize or stem
    if stem_or_lem == "lem" and lemmatizer:
        tokens = [lemmatizer.lemmatize(w) for w in tokens]
    elif stem_or_lem != "lem" and stemmer:
        tokens = [stemmer.stem(w) for w in tokens]

    return ' '.join(tokens).strip()
