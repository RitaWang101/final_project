import pandas as pd
import praw
from datetime import datetime, timezone
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# ─── Configuration ────────────────────────────────────────────
SUBREDDITS    = ["iPhone13", "iPhoneXR"]
POST_LIMIT    = 10_000      # max posts per subreddit
MAX_COMMENTS  = 5           # per post
KEYWORDS      = [
    "battery","system","camera","charging","screen","face id",
    "design","performance","ios","storage","faceid","touchid",
    "speakers","siri","imessage","icloud","5g","privacy",
    "water resistant","ui","ux"
]
OUTPUT_CSV    = "reddit_iphone13XR_data.csv"


def fetch_data() -> pd.DataFrame:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    records = []
    for sub in SUBREDDITS:
        print(f"[+] Fetching from r/{sub}…")
        for post in reddit.subreddit(sub).hot(limit=POST_LIMIT):
            if post.stickied:
                continue

            text = f"{post.title} {post.selftext}".lower()
            if not any(kw.lower() in text for kw in KEYWORDS):
                continue

            # collect comments
            post.comments.replace_more(limit=0)
            comments = [c.body for c in post.comments[:MAX_COMMENTS] if getattr(c, "body", None)]

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
            # attach comment_1…comment_5
            for i in range(MAX_COMMENTS):
                rec[f"comment_{i+1}"] = comments[i] if i < len(comments) else ""
            records.append(rec)

    return pd.DataFrame(records) 
#Main     
if __name__ == "__main__":
    df = fetch_data()
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"[✓] Saved to {OUTPUT_CSV} ({len(df)} rows)")
