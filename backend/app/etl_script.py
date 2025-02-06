from extractors.twitter_extractor import TwitterExtractor
from transformers.sentiment_analyzer import SentimentAnalyzer
from loaders.postgres_loader import PostgresLoader
import pandas as pd
import time

def run_etl_pipeline():
    while True:
        try:
            # Extract
            twitter = TwitterExtractor()
            mentions = twitter.extract_mentions("your_brand_name")
            
            if mentions:
                # Transform
                mentions_df = pd.DataFrame(mentions)
                analyzer = SentimentAnalyzer()
                analyzed_df = analyzer.analyze_texts(mentions_df)
                
                # Load
                loader = PostgresLoader()
                loader.load_data(analyzed_df, 'social_mentions')
            
            # Wait for 5 minutes before next extraction
            time.sleep(300)
            
        except Exception as e:
            print(f"Error in ETL pipeline: {e}")
            time.sleep(60)  # Wait 1 minute before retry

if __name__ == "__main__":
    print("Starting ETL pipeline...")
    run_etl_pipeline() 