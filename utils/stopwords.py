import nltk
from nltk.corpus import stopwords

# Download stopwords lần đầu tiên (chạy 1 lần thôi)
# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def is_stopword(word: str) -> bool:
    return word.lower() in stop_words

def remove_stopwords(tokens: list[str]) -> list[str]:
    return [token for token in tokens if not is_stopword(token)]
