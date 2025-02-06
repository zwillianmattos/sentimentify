-- Create the etl_sentimentify database
CREATE DATABASE etl_sentimentify;

-- Connect to the etl_sentimentify database
\c etl_sentimentify;

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum for sentiment types
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sentiment_type') THEN
        CREATE TYPE sentiment_type AS ENUM ('positive', 'negative', 'neutral');
    END IF;
END$$;

-- Create table for social media mentions
CREATE TABLE IF NOT EXISTS social_mentions (
    id SERIAL PRIMARY KEY,
    mention_id VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    location VARCHAR(255),
    source VARCHAR(50) NOT NULL,
    polarity FLOAT NOT NULL,
    subjectivity FLOAT NOT NULL,
    sentiment sentiment_type NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_social_mentions_sentiment ON social_mentions(sentiment);
CREATE INDEX IF NOT EXISTS idx_social_mentions_created_at ON social_mentions(created_at);
CREATE INDEX IF NOT EXISTS idx_social_mentions_source ON social_mentions(source);

-- Create table for brands/keywords being monitored
CREATE TABLE IF NOT EXISTS monitored_terms (
    id SERIAL PRIMARY KEY,
    term VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for sentiment statistics
CREATE TABLE IF NOT EXISTS sentiment_stats (
    id SERIAL PRIMARY KEY,
    term_id INTEGER REFERENCES monitored_terms(id),
    date DATE NOT NULL,
    positive_count INTEGER DEFAULT 0,
    negative_count INTEGER DEFAULT 0,
    neutral_count INTEGER DEFAULT 0,
    average_polarity FLOAT,
    average_subjectivity FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(term_id, date)
);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_monitored_terms_updated_at ON monitored_terms;
CREATE TRIGGER update_monitored_terms_updated_at
    BEFORE UPDATE ON monitored_terms
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert some initial monitored terms
INSERT INTO monitored_terms (term) VALUES
    ('your_brand_name'),
    ('your_product_name'),
    ('your_competitor_name')
ON CONFLICT DO NOTHING; 