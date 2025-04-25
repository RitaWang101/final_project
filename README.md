# iPhone Consumer Insights Analysis

## Introduction
This project digs into real-world consumer insights for the iPhone by analyzing user-generated reviews from various e-commerce platforms and Reddit. It combines structured product attributes with unstructured customer feedback to:

- Identify patterns in customer sentiment and behavioral feedback  
- Assess product satisfaction across different iPhone models and markets  
- Explore correlations between product features and user satisfaction  

The analysis focuses on cross-platform consistency, review behavior patterns, and feature-related sentiment trends using data collection, parsing, transformation, analysis, and visualization techniques.

## Data Sources

1. **Apple iPhone XR Reviews (Amazon.com)**  
   - **Source:** [Kaggle: Apple iPhone 11 Reviews](https://www.kaggle.com/datasets/thedevastator/apple-iphone-11-reviews-from-amazon-com)  
   - **Description:** CSV with over 30,000 reviews for Apple iPhone 11 on Amazon.com  
   - **Fields (3,000 rows):**  
     `productAsin`, `country`, `date`, `isVerified`, `ratingScore`,  
     `reviewTitle`, `reviewDescription`, `variant`, `variantAsin`, `reviewUrl`

2. **Apple iPhone 13 Reviews (Amazon India)**  
   - **Source:** Local CSV (`iphone13.csv`)  
   - **Description:** Customer reviews for Apple iPhone 13 on Amazon India  
   - **Fields (5,000 rows):**  
     `product`, `review_text`, `review_rating`, `helpful_count`, `total_comments`,  
     `reviewed_at`, `review_country`, `review_title`, `url`, `profile_name`

3. **Reddit Discussions**  
   - **Subreddits:** `r/iPhoneXR` and `r/iPhone13`  
   - **Description:** 600 comments combined  
   - **Fields:** `thread_title`, `comment_id`, `content`, `subreddit`, `author`

## Analysis Steps

1. **Data Collection & Cleaning**  
   - Automated scraping of Reddit via PRAW  
   - Standardize timestamps and clean text fields  

2. **Keyword Sentiment Analysis**  
   - Extract features from `features_in_post`  
   - Map features to `post_sentiment` scores  
   - Compute and rank average sentiment per feature (≥2 occurrences)  
   - Visualize top 10 features by average sentiment  

3. **Time-Based Sentiment Analysis**  
   - Convert `created_time` to daily and monthly bins  
   - Compute daily post counts and daily average sentiment  
   - Compute monthly average sentiment  
   - Plot daily posts vs. sentiment and monthly sentiment trends  

4. **Keyword Frequency Comparison**  
   - Count keyword occurrences per subreddit  
   - Identify common vs. unique keywords  
   - Visualize top 10 unique and common keywords for each model  

## Summary of Results

- **Top Features by Sentiment:** _[Your brief findings here]_  
- **Sentiment Over Time:** _[Key trend insights here]_  
- **Keyword Differences:** _[Highlights of shared vs. unique terms]_  

## How to Run

1. **Clone the repo**  
   ```bash
   git clone <repo-url>
   cd <repo-directory>
2. **Install Library**
   ```bash
   pip install -r requirements.txt
3. **Configure API keys (create a .env file)**
   ```bash
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   USER_AGENT=your_user_agent
