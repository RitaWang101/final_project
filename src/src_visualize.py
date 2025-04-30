import pandas as pd
import seaborn as sns
from ast import literal_eval
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 
from ast import literal_eval 

# F 1. Function to visualize Cross-Version Reddit Sentiment Analysis: 
def visualize_top_features(feature_ave_sent, subreddit_name):

    # Sort by frequency for visualization and take the top 10
    sorted_feature = sorted(feature_ave_sent.items(), key=lambda x: x[1], reverse=True)[:10]
    
    keywords, ave_sentiments = zip(*sorted_feature)
    
    sorted_feature = sorted(feature_ave_sent.items(), key=lambda x: x[1], reverse=True)[:10] #从大到小取最大的10个

    keywords, ave_sentiments = zip(*sorted_feature) 
    # Plot the keywords and the average sentiments
    plt.figure(figsize=(10, 6))
    plt.bar(keywords, ave_sentiments, color='lightblue')
    plt.title(f'Top 10 Product Features by Average Sentiment for {subreddit_name}')
    plt.xlabel('Product Features')
    plt.ylabel('Average Sentiment')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'top_10_product_features_by_average_sentiment_{subreddit_name}.png')
    plt.show() 

#2.Visualize the Keyword frequency by subreddit
import matplotlib.pyplot as plt

def plot_common_keyword_freq(
    df_common,
    sub1: str = 'iPhone13',
    sub2: str = 'iPhoneXR',
    figsize: tuple = (10,6),
    save_path: str = None
):

    df_plot = df_common.set_index('Keyword')
    ax = df_plot.plot(
        kind='bar',
        figsize=figsize
    )
    ax.set_title(f'Common Features Frequency: {sub1} vs. {sub2}')
    ax.set_ylabel('Frequency')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='right')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    plt.show()


    
#3.Function to visualize the plot of the relationship between time and sentiment for a given subreddit.
def compare_time_sentiment(df):
    # Compute metrics
    m13 = analyze_time_sentiment(df, 'iPhone13')
    mxr = analyze_time_sentiment(df, 'iPhoneXR')

    # Align months
    months = sorted(set(m13['monthly_posts'].index) | set(mxr['monthly_posts'].index))
    p13 = m13['monthly_posts'].reindex(months, fill_value=0)
    pxr = mxr['monthly_posts'].reindex(months, fill_value=0)
    s13 = m13['monthly_sentiment'].reindex(months)
    sxr = mxr['monthly_sentiment'].reindex(months)

    # Plot
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(14,8), sharex=True)

    # Top: post counts
    ax1.plot(months, p13, 'o-', label='iPhone13', color='tab:blue')
    ax1.plot(months, pxr, 's-', label='iPhoneXR',  color='tab:green')
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('Monthly Posts')
    ax1.legend(loc='upper left')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # Bottom: avg sentiment
    ax2.plot(months, s13, 'o-', label='iPhone13', color='tab:orange')
    ax2.plot(months, sxr, 's-', label='iPhoneXR',  color='tab:red')
    ax2.set_ylim(-1, 1)
    ax2.set_ylabel('Avg Sentiment')
    ax2.legend(loc='upper left')
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_xlabel('Year-Month')

    plt.xticks(rotation=45, ha='right')
    plt.suptitle('r/iPhone13 vs r/iPhoneXR: Posts & Sentiment Over Time')
    plt.tight_layout(rect=[0,0,1,0.95])
    filename = f'iPhone13 vs iPhoneXR: Posts & Sentiment Over Time.png'
    plt.savefig(filename)
    plt.show() 




#4(1). Visualize the Cross-Platform comparison of post_sentiment only group by platform

def plot_avg_sentiment_by_platform(df: pd.DataFrame,
                                   platform_col: str = 'platform',
                                   sentiment_col: str = 'post_sentiment',
                                   figsize: tuple = (6,4),
                                   colors: list = ['skyblue','salmon']):
  
    avg_sent = (
        df
          .groupby(platform_col, as_index=False)[sentiment_col]
          .mean()
          .rename(columns={sentiment_col: 'avg_sentiment'})
    )

    plt.figure(figsize=figsize)
    plt.bar(avg_sent[platform_col], avg_sent['avg_sentiment'], color=colors[:len(avg_sent)])
    plt.title('Average Post Sentiment by Platform')
    plt.xlabel('Platform')
    plt.ylabel('Average Sentiment Score')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

    return avg_sent 


#4(2). Visualize the Cross-Platform comparison of post_sentiment only group by both platform and version 

def plot_avg_sentiment_by_platform_version(
    df: pd.DataFrame,
    platform_col: str = 'platform',
    version_col: str = 'iphone_version',
    sentiment_col: str = 'post_sentiment',
    figsize: tuple = (8,5),
    colors: list = ['skyblue','salmon']
) -> pd.DataFrame:
    avg_sent = (
        df
          .groupby([platform_col, version_col], as_index=False)[sentiment_col]
          .mean()
          .rename(columns={sentiment_col: 'avg_sentiment'})
    )

    pivot = avg_sent.pivot(
        index=version_col,
        columns=platform_col,
        values='avg_sentiment'
    )

    pivot.plot(
        kind='bar',
        figsize=figsize,
        color=colors[:pivot.shape[1]]
    )
    plt.title('Average Sentiment by Platform & iPhone Version')
    plt.xlabel('iPhone Version')
    plt.ylabel('Average Sentiment Score')
    plt.ylim(0, 1)
    plt.xticks(rotation=0)
    plt.legend(title='Platform')
    plt.tight_layout()
    plt.show()

    return pivot


#5. Visualize the CDF of Amazon Rating Scores

def plot_rating_cdf(
    xr_sorted, xr_cdf,
    x13_sorted, x13_cdf,
    labels=('iPhone XR','iPhone 13'),
    colors=('tab:red','tab:blue'),
    figsize=(10,6)
):

    plt.figure(figsize=figsize)
    plt.step(xr_sorted,  xr_cdf,  where='post', label=labels[0], color=colors[0])
    plt.step(x13_sorted, x13_cdf, where='post', label=labels[1], color=colors[1])

    plt.title('CDF of Amazon Rating Scores: iPhone XR vs. iPhone 13')
    plt.xlabel('Rating Score')
    plt.ylabel('Cumulative Proportion of Reviews')
    plt.xticks([1, 2, 3, 4, 5])
    plt.legend()
    plt.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

#6. AMAZON Visualize: SCORE AND KEYWORDS RELATION 
def plot_feature_rating_stats(
    stats_df: pd.DataFrame,
    title: str = 'Average Rating Score by Feature',
    figsize: tuple = (12,6),
    bar_color: str = 'skyblue',
    bar_width: float = 0.6
):

    plt.figure(figsize=figsize)
    plt.bar(
        stats_df.index,
        stats_df['mean'],
        color=bar_color,
        width=bar_width
    )
    plt.title(title)
    plt.ylabel('Average Rating Score')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

