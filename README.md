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
   - **Description:** 1170 comments combined  
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
   - Convert `created_time` to monthly bins  
   - Compute daily post counts and daily average sentiment  
   - Compute monthly average sentiment  
   - Plot daily posts vs. sentiment and monthly sentiment trends  

4. **Keyword Frequency Comparison**  
   - Count keyword occurrences per subreddit  
   - Identify common vs. unique keywords  
   - Visualize top 10 unique and common keywords for each model
5. **Cross Platform Analysis**
   - create a new table called combined only including sentiment score and platform as well as iphone version
   - group by platform and iphone version to calculate the mean score of sentiment 

## Results Summary

### 1. Reddit Keyword Frequency  
- **Battery** and **iOS** dominate both communities:  
- **Camera** is more prevalent in r/iPhone13 (~65 vs. ~51), while **screen** ranks third in both (13 ≈ 87; XR ≈ 113).  
- XR users show higher relative concern most of the features than 13 users.

### 2. Cross-Version Sentiment (Reddit)  
- **iPhone XR** top-sentiment features:  
  - **camera** and **battery**  
- **iPhone 13** top-sentiment features:  
  - **5G**and **system (iOS stability)**
- Emerging positive mentions: **Face ID** (avg 0.123) and **iMessage** (avg 0.09)
- Users feel negative on camera gradually and batetty, but **screen** always can not meet users'satisfaction 

### 3. Activity & Sentiment Over Time  
- r/iPhone13 surged to 100 posts in January 2025, then stabilized around 38/month.  
- XR sentiment remains positive (+0.05 to +0.20); 13 began negative (–0.10 at launch), crossed neutral in December 2024, and settled around +0.10 by Q1 2025.

### 4. Amazon Rating Comparison  
- **iPhone XR** leads on **performance** and **software stability**.  
- **iPhone 13** leads on **storage capacity** and **audio**.  
- Both models score lowest on **screen** and **charging**, which is consistent with the sentiment reflection in Reddit 
- iPhone 13 reviewers have new concern about **Privacy** 

### 5. Cross-Platform Sentiment  
- Amazon reviews average ~0.38 sentiment versus Reddit’s ~0.08.  
- By model:  
   1. people are willing to show positive sentiment on the **e-commerce website** and talk about real concern on **forum**
   2. Especially in the **XR** using experience, the sentiment score show a large gap between the two platform 
   
  
## How to Run

1. **Clone the repo**  
   ```bash
   cd ~/Desktop
   git clone <repo-url> # the github url
   cd ~/Desktop/final_project 
2. **Install Library**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
3. **Configure API keys (create a .env file in src folder,cpy these to .env in scr folder)**
   ```bash
   REDDIT_CLIENT_ID=your_reddit_client_id_here
   REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
   REDDIT_USER_AGENT=your_reddit_user_agent_here
   KAGGLE_USERNAME=your_kaggle_username_here
   KAGGLE_KEY=your_kaggle_key_here
4. **run result.ipynb**
   ```bash
   jupyter notebook result.ipynb 
