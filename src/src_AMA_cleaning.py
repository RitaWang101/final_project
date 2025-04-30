import re
import pandas as pd
from textblob import TextBlob
#XR CLEANING
def clean_ama_xr_reviews(
    input_csv: str = 'apple_iphone_XR_reviews.csv',
    output_csv: str = 'testAMA_XR_ iphonecleaned.csv',
    feature_keywords: list = None
) -> pd.DataFrame:

    # Default feature keywords if none provided
    if feature_keywords is None:
        feature_keywords = [
            'battery','system','camera','charging','screen','face id',
            'design','performance','ios','storage','faceid','touchid',
            'speakers','siri','imessage','icloud','5g','privacy',
            'water resistant','ui','ux'
        ]

    df = pd.read_csv(input_csv)

    # Helper functions
    def clean_text(text: str) -> str:
        if not isinstance(text, str):
            return ""
        t = text.strip().lower().replace("\n", " ").replace("\r", "")
        t = re.sub(r'http[s]?://\S+|www\S+', '', t)
        t = re.sub(r'[^\x00-\x7F]+', '', t)
        t = re.sub(r'\W', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    def is_valid_text(text: str) -> bool:
        if not isinstance(text, str):
            return False
        t = text.strip().lower()
        return len(t) >= 15 and t not in ["[deleted]", "[removed]"]

    def extract_features(text: str) -> list:
        t = (text or "").lower()
        return [kw for kw in feature_keywords if kw in t]

    def get_sentiment(text: str) -> float:
        return TextBlob(text).sentiment.polarity if isinstance(text, str) else 0.0

    def extract_rating(text: str) -> float:
        m = re.search(r'(\d+\.\d+)', str(text))
        return float(m.group(1)) if m else None

    # Apply cleaning pipeline
    df['review_text']     = df['review_text'].map(clean_text)
    df['valid_text']      = df['review_text'].map(is_valid_text)
    df['review_title']    = df['review_title'].map(clean_text)
    df['valid_title']     = df['review_title'].map(is_valid_text)
    df['features_in_post']  = df['review_text'].map(extract_features)
    df['features_in_title'] = df['review_title'].map(extract_features)
    df['post_sentiment']  = df['review_text'].map(get_sentiment)
    df['title_sentiment'] = df['review_title'].map(get_sentiment)
    df['ratingScore']     = df['review_rating'].map(extract_rating)

    # Write out and return
    df.to_csv(output_csv, index=False)
    print(f"[+] Cleaned {len(df)} records → {output_csv}")
    return df


# AMAZON 13 CLEANING
FEATURE_KEYWORDS = [
    'battery','system','camera','charging','screen','face id',
    'design','performance','ios','storage','faceid','touchid',
    'speakers','siri','imessage','icloud','5g','privacy',
    'water resistant','ui','ux'
]

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    t = text.strip().lower().replace("\n", " ").replace("\r", "")
    t = re.sub(r'http[s]?://\S+|www\S+', '', t)
    t = re.sub(r'[^\x00-\x7F]+', '', t)
    t = re.sub(r'\W', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def is_valid_text(text: str) -> bool:
    if not isinstance(text, str):
        return False
    t = text.strip().lower()
    return len(t) >= 15 and t not in ("[deleted]", "[removed]")

def extract_features(text: str) -> list[str]:
    txt = (text or "").lower()
    return [kw for kw in FEATURE_KEYWORDS if kw in txt]

def get_sentiment(text: str) -> float:
    return TextBlob(text).sentiment.polarity if isinstance(text, str) else 0.0

def clean_ama13_reviews(
    input_csv: str = 'iphone13.csv',
    output_csv: str = 'testAMA13_ iphonecleaned.csv'
) -> pd.DataFrame:
    """
    Cleans the iPhone 13 Amazon reviews CSV:
      - normalizes text/title
      - filters too-short entries
      - extracts keyword features
      - computes sentiment scores

    Args:
      input_csv  : path to raw iphone13.csv
      output_csv : path to write cleaned CSV

    Returns:
      Cleaned DataFrame.
    """
    df = pd.read_csv(input_csv)

    # Clean and validate text & title
    df['review_text']  = df['reviewDescription'].map(clean_text)
    df['valid_text']   = df['review_text'].map(is_valid_text)
    df['review_title'] = df['reviewTitle'].map(clean_text)
    df['valid_title']  = df['review_title'].map(is_valid_text)

    # Feature extraction
    df['features_in_post'] = df['review_text'].map(extract_features)

    # Sentiment
    df['post_sentiment'] = df['review_text'].map(get_sentiment)

    # Save and return
    df.to_csv(output_csv, index=False)
    print(f"[+] Cleaned {len(df)} rows → {output_csv}")
    return df
