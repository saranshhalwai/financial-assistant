import yfinance as yf
from crewai_tools import tool
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

@tool
def sentiment_analysis(ticker: str):
    """
    Perform sentiment analysis on recent news articles about the given stock.
    
    Args:
        ticker (str): The stock ticker symbol.
    
    Returns:
        dict: Sentiment analysis results.
    """
    # Fetch recent news articles
    stock = yf.Ticker(ticker)
    news = stock.news
    
    sentiments = []
    for article in news[:5]:  # Analyze the 5 most recent articles
        title = article['title']
        blob = TextBlob(title)
        sentiment = blob.sentiment.polarity
        sentiments.append(sentiment)
    
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    
    # Fetch social media sentiment (simulated)
    social_sentiment = simulate_social_sentiment(ticker)
    
    return {
        "ticker": ticker,
        "news_sentiment": avg_sentiment,
        "social_sentiment": social_sentiment,
        "overall_sentiment": (avg_sentiment + social_sentiment) / 2
    }

def simulate_social_sentiment(ticker):
    # This is a placeholder for actual social media sentiment analysis
    # In a real-world scenario, you would use APIs from Twitter, StockTwits, etc.
    import random
    return random.uniform(-1, 1)
