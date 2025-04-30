import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    raise FileNotFoundError(f".env not found at {env_path}")
load_dotenv(dotenv_path=env_path)

REDDIT_CLIENT_ID     = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT    = os.environ.get("REDDIT_USER_AGENT")

KAGGLE_USERNAME = os.environ.get("KAGGLE_USERNAME")
KAGGLE_KEY      = os.environ.get("KAGGLE_KEY")
# 4️⃣ Validate that all required variables are set
required = [
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USER_AGENT",
    "KAGGLE_USERNAME",
    "KAGGLE_KEY"
]
for var in required:
    if not os.environ.get(var):
        raise EnvironmentError(f"{var} not set in env.txt") 
