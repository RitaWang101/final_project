import re
import pandas as pd
import numpy as np
from textblob import TextBlob

FEATURE_KEYWORDS = [
    'battery','system','camera','charging','screen','face id',
    'design','performance','ios','storage','faceid','touchid',
    'speakers','siri','imessage','icloud','5g','privacy',
    'water resistant','ui','ux'
]

def clean_reddit_comments(
    input_csv: str = 'reddit_iphone13XR_data.csv',
    output_csv: str = 'newreddit_iphone13XRcleaned.csv',
    max_comments: int = 5
) -> pd.DataFrame:
    df = pd.read_csv(input_csv)

    def clean_text(text):
        if not isinstance(text, str):
            return ""
        t = text.strip().lower().replace("\n", " ").replace("\r", "")
        t = re.sub(r'http\S+|www\S+', "", t)
        t = re.sub(r"[^\x00-\x7F]+", "", t)
        t = re.sub(r"\W", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def is_valid_text(text):
        if not isinstance(text, str):
            return False
        t = text.strip().lower()
        return len(t) >= 15 and t not in ("[deleted]", "[removed]")

    def extract_features(text):
        txt = (text or "").lower()
        return [kw for kw in FEATURE_KEYWORDS if kw in txt]

    def get_sentiment(text):
        return TextBlob(text).sentiment.polarity if isinstance(text, str) else 0.0

    # Clean the main post content
    df['content'] = df['content'].map(clean_text)
    df = df[df['content'].map(is_valid_text)]

    # Clean each comment column
    for i in range(1, max_comments+1):
        col = f'comment_{i}'
        if col in df.columns:
            df[col] = df[col].map(clean_text)
            df = df[df[col].map(lambda t: t=="" or is_valid_text(t))]

    # Feature extraction
    df['features_in_post'] = df['content'].map(extract_features)
    for i in range(1, max_comments+1):
        col = f'comment_{i}'
        if col in df.columns:
            df[f'features_in_{col}'] = df[col].map(extract_features)

    # Sentiment
    df['post_sentiment'] = df['content'].map(get_sentiment)
    for i in range(1, max_comments+1):
        col = f'comment_{i}'
        if col in df.columns:
            df[f'{col}_sentiment'] = df[col].map(get_sentiment)

    # Save and return
    df.to_csv(output_csv, index=False)
    print(f"[+] Cleaned Reddit data: {len(df)} rows → {output_csv}")
    return df


if __name__ == "__main__":
    clean_reddit_comments() 

