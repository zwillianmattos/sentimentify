from textblob import TextBlob
import pandas as pd

class SentimentAnalyzer:
    def analyze_texts(self, texts_df):
        """
        Analyze sentiment of texts using TextBlob
        Returns DataFrame with sentiment scores
        """
        def get_sentiment(text):
            analysis = TextBlob(str(text))
            # Returns polarity (-1 to 1) and subjectivity (0 to 1)
            return pd.Series([
                analysis.sentiment.polarity,
                analysis.sentiment.subjectivity,
                self._get_sentiment_label(analysis.sentiment.polarity)
            ])
        
        # Apply sentiment analysis to each text
        sentiment_scores = texts_df['text'].apply(get_sentiment)
        sentiment_scores.columns = ['polarity', 'subjectivity', 'sentiment']
        
        return pd.concat([texts_df, sentiment_scores], axis=1)
    
    def _get_sentiment_label(self, polarity):
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral' 