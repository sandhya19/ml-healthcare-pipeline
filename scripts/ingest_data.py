# scripts/ingest_data.py

import feedparser
import boto3
import json
from datetime import datetime
import os

# CONFIGURATION
RSS_FEED_URL = 'https://digitalhealth.net/feed/'  # Example healthcare RSS feed
S3_BUCKET_NAME = 'ml-healthcaredata-pipeline'
S3_FOLDER = 'raw_data/'  # where to store in the bucket
AWS_REGION = 'eu-west-2'  # e.g., London region

# AWS S3 Client
s3 = boto3.client('s3', region_name=AWS_REGION)

def fetch_rss_feed(url):
    """Fetch articles from RSS feed."""
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
        })
    return articles

def save_to_s3(data, bucket, key):
    """Save data to S3 bucket."""
    json_data = json.dumps(data)
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json_data,
        ContentType='application/json'
    )
    print(f"Saved {len(data)} articles to s3://{bucket}/{key}")

def main():
    articles = fetch_rss_feed(RSS_FEED_URL)

    if not articles:
        print("No articles fetched.")
        return

    # Generate filename based on current date
    today = datetime.utcnow().strftime('%Y-%m-%d')
    file_name = f"{S3_FOLDER}healthcare_news_{today}.json"

    save_to_s3(articles, S3_BUCKET_NAME, file_name)

if __name__ == "__main__":
    main()