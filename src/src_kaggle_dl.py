# src/src_kaggle_dl.py

import os
from config import KAGGLE_USERNAME, KAGGLE_KEY

def download_kaggle_datasets():
    os.environ["KAGGLE_USERNAME"] = KAGGLE_USERNAME
    os.environ["KAGGLE_KEY"]      = KAGGLE_KEY
    cmds = [
        # download & unzip iPhone customer reviews
        "kaggle datasets download -d mrmars1010/iphone-customer-reviews-nlp -p .",
        "unzip -o iphone-customer-reviews-nlp.zip",
        "rm iphone-customer-reviews-nlp.zip",

        # download & unzip iPhone 11 Amazon reviews
        "kaggle datasets download -d thedevastator/apple-iphone-11-reviews-from-amazon-com -p .",
        "unzip -o apple-iphone-11-reviews-from-amazon-com.zip",
        "rm apple-iphone-11-reviews-from-amazon-com.zip",
    ]

    for cmd in cmds:
        print(f">>> {cmd}")
        os.system(cmd)

    print("✅ Downloaded and unzipped both Kaggle datasets.")

if __name__ == "__main__":
    download_kaggle_datasets()
