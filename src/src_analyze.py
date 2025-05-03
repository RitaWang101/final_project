import pandas as pd
import seaborn as sns
from ast import literal_eval
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas as pd
from ast import literal_eval
import wordcloud 


# 1. Function to analyze Cross-Version Reddit Sentiment Analysis: 
def analyze_keywords_sentiment(df, subreddit_name):

    # Filter DataFrame based on subreddit
    df_sub = df[df['subreddit'] == subreddit_name]
    
    # Initialize dictionary to store feature sentiment
    feature_sentiment = {} 
    
    # Iterate through rows to collect features and their corresponding sentiments
    for _, row in df_sub.iterrows():
        post_sent = row['post_sentiment']
        features = row.get('features_in_post', None)
        if isinstance(features, str):
            try:
                keywords = literal_eval(features)
            except (ValueError, SyntaxError):
                continue
        elif isinstance(features, list):
            keywords = features
        else:
            continue
        for kw in keywords:
            feature_sentiment.setdefault(kw, []).append(post_sent)

    # Calculate average sentiment for features with at least 2 sentiments
    feature_ave_sent = {k: np.mean(v) for k, v in feature_sentiment.items() if len(v) >= 2}

    # Return the dictionary of features and their average sentiment
    return feature_ave_sent



#2. KeyWord Frequency Analysis 
import pandas as pd
from ast import literal_eval
from collections import Counter

def count_keywords(subreddit_df: pd.DataFrame, feature_col: str = 'features_in_post') -> Counter:

    keyword_list = []
    for item in subreddit_df[feature_col]:
        if pd.notna(item):
            keyword_list += literal_eval(item)
    return Counter(keyword_list)


def build_common_keyword_df(
    df: pd.DataFrame,
    sub1: str = 'iPhone13',
    sub2: str = 'iPhoneXR'
) -> pd.DataFrame:

    # Count per-subreddit
    kw1 = count_keywords(df[df['subreddit'] == sub1])
    kw2 = count_keywords(df[df['subreddit'] == sub2])

    # Intersection
    common = set(kw1.keys()) & set(kw2.keys())

    # Build DF
    data = [
        {'Keyword': k,
         f'Freq_{sub1}': kw1[k],
         f'Freq_{sub2}': kw2[k]}
        for k in common
    ]
    df_common = pd.DataFrame(data)
    df_common['Total'] = df_common[f'Freq_{sub1}'] + df_common[f'Freq_{sub2}']

    # Top 10
    df_top = (
        df_common
          .sort_values('Total', ascending=False)
          .head(10)
          .drop(columns='Total')
          .reset_index(drop=True)
    )
    return df_top
 


#3.This function analyzes the relationship between time and sentiment for a given subreddit.
def analyze_time_sentiment(df, subreddit_name):
    df_sub = df[df['subreddit'] == subreddit_name].copy()
    df_sub['create_time'] = pd.to_datetime(df_sub['created_time'])
    df_sub['year_month'] = df_sub['create_time'].dt.strftime('%Y-%m')
    monthly_posts     = df_sub.groupby('year_month').size()
    monthly_sentiment = df_sub.groupby('year_month')['post_sentiment'].mean()
    return {'monthly_posts': monthly_posts, 'monthly_sentiment': monthly_sentiment} 



#4.This function analyze the cross-platform comparison of post_sentiment 
def build_balanced_sample(
    ama13_path: str,
    ama_xr_path: str,
    reddit_path: str,
    n: int = 200,
    random_state: int = 42
) -> pd.DataFrame:

    ama13  = pd.read_csv(ama13_path)
    ama_xr = pd.read_csv(ama_xr_path)
    reddit = pd.read_csv(reddit_path)
    
    if 'post' in ama13.columns and 'post_sentiment' not in ama13.columns:
      ama13 = ama13.rename(columns={'post': 'post_sentiment'})
    # 2. Annotate
    ama13['platform']        = 'Amazon'
    ama13['iphone_version']  = 'iPhone13'
    ama_xr['platform']       = 'Amazon'
    ama_xr['iphone_version'] = 'iPhoneXR'
    reddit['platform']       = 'Reddit'
    reddit['iphone_version'] = reddit['subreddit']
    

    def sample_n(df):
        return df.sample(n=min(len(df), n), random_state=random_state)
    
  
    s_ama13 = sample_n(ama13)[['platform','iphone_version','post_sentiment']]
    s_amaxr = sample_n(ama_xr)[['platform','iphone_version','post_sentiment']]
    s_r13   = sample_n(reddit[reddit['iphone_version']=='iPhone13'])[['platform','iphone_version','post_sentiment']]
    s_rxr   = sample_n(reddit[reddit['iphone_version']=='iPhoneXR'])[['platform','iphone_version','post_sentiment']]
    
   
    combined = pd.concat([s_ama13, s_amaxr, s_r13, s_rxr], ignore_index=True)
    return combined 


#5.The CDF of Amazon Rating Scores Analysis 
import numpy as np
import pandas as pd

def compute_rating_cdfs(
    df_xr: pd.DataFrame,
    df_13: pd.DataFrame,
    score_col: str = 'ratingScore'
):

    xr_scores = pd.to_numeric(df_xr[score_col], errors='coerce').dropna().values.astype(float)
    x13_scores = pd.to_numeric(df_13[score_col], errors='coerce').dropna().values.astype(float)

    xr_sorted = np.sort(xr_scores)
    x13_sorted = np.sort(x13_scores)

    xr_cdf  = np.arange(1, len(xr_sorted)+1) / len(xr_sorted)
    x13_cdf = np.arange(1, len(x13_sorted)+1) / len(x13_sorted)

    return xr_sorted, xr_cdf, x13_sorted, x13_cdf



#6. AMAZON ANALYSIS: SCORE AND KEYWORDS RELATION 
import pandas as pd
from ast import literal_eval

def compute_feature_rating_stats(
    df: pd.DataFrame,
    feature_col: str = 'features_in_post',
    score_col: str = 'ratingScore',
    min_count: int = 10
) -> pd.DataFrame:

    df = df.copy()
    def _parse_feats(x):
        if isinstance(x, str):
            try:
                return literal_eval(x)
            except (ValueError, SyntaxError):
                return []
        elif isinstance(x, list):
            return x
        else:
            return []

    df['prod_features'] = df[feature_col].apply(_parse_feats)    
    df_exp = df.explode('prod_features')
    
    df_exp[score_col] = pd.to_numeric(df_exp[score_col], errors='coerce')
    
    stats = (
        df_exp
          .groupby('prod_features')[score_col]
          .agg(['mean','count'])
          .rename_axis('feature')
    )
    
    stats = stats[stats['count'] > min_count]
    stats = stats.sort_values('mean', ascending=False)
    
    return stats  

