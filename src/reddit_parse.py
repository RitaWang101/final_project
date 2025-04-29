# src/reddit_parse.py
import pandas as pd
import praw
from datetime import datetime, timezone
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def parse_reddit(
    subreddits   = ["iPhone13", "iPhoneXR"],
    keywords     = [
        "battery","system","camera","charging","screen","face id",
        "design","performance","ios","storage","faceid","touchid",
        "speakers","siri","imessage","icloud","5g","privacy",
        "water resistant","ui","ux"
    ],
    post_limit   = 10000,
    max_comments = 5,
    output_csv   = "reddit_iphone13XR_data.csv"
) -> pd.DataFrame:
    records = []
    for sub in subreddits:
        for post in reddit.subreddit(sub).hot(limit=post_limit):
            if post.stickied:
                continue
            text = (post.title + " " + post.selftext).lower()
            if not any(kw.lower() in text for kw in keywords):
                continue

            post.comments.replace_more(limit=0)
            bodies = [c.body for c in post.comments[:max_comments]
                      if getattr(c, "body", None)]

            rec = {
                "subreddit":    sub,
                "post_id":      post.id,
                "title":        post.title,
                "content":      post.selftext,
                "created_time": datetime.fromtimestamp(
                                     post.created_utc, tz=timezone.utc
                                 ).strftime("%Y-%m-%d %H:%M:%S"),
                "num_comments": post.num_comments,
                "url":          post.url
            }
            for i in range(max_comments):
                rec[f"comment_{i+1}"] = bodies[i] if i < len(bodies) else ""
            records.append(rec)

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    return df
