import pandas as pd
import praw
from datetime import datetime, timezone
from src.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

SUBREDDITS   = ["iPhone13","iPhoneXR"]
POST_LIMIT   = 10000
MAX_COMMENTS = 5
KEYWORDS     = [
    "battery","system","camera","charging","screen","face id",
    "design","performance","ios","storage","faceid","touchid",
    "speakers","siri","imessage","icloud","5g","privacy",
    "water resistant","ui","ux"
]
OUTPUT_CSV   = "reddit_iphone13XR_data.csv"


def fetch_data() -> pd.DataFrame:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    records = []
    for sub in SUBREDDITS:
        for post in reddit.subreddit(sub).hot(limit=POST_LIMIT):
            if post.stickied: continue
            text = (post.title + post.selftext).lower()
            if not any(kw in text for kw in KEYWORDS): continue
            post.comments.replace_more(limit=0)
            comments = [c.body for c in post.comments[:MAX_COMMENTS]]
            rec = {
                "subreddit": sub,
                "post_id": post.id,
                "title": post.title,
                "content": post.selftext,
                "created_time": datetime.fromtimestamp(post.created_utc, tz=timezone.utc),
                "num_comments": post.num_comments,
                "url": post.url
            }
            for i in range(MAX_COMMENTS): rec[f"comment_{i+1}"] = comments[i] if i<len(comments) else ""
            records.append(rec)
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)
    return df  
