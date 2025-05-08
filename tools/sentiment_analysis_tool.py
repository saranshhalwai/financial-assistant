# import tweepy
import yfinance as yf
from dotenv import load_dotenv
from langchain.tools import tool
from textblob import TextBlob

load_dotenv()


# Initialize Tweepy client (replace with your actual credentials or use environment variables)
# TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")  # Secure way to store credentials
#
# client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)


@tool
def sentiment_analysis(ticker: str):
    """
    Perform sentiment analysis on recent news and tweets about the given stock.
    
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
        title = article['content']['title']
        blob = TextBlob(title)
        sentiment = blob.sentiment.polarity
        sentiments.append(sentiment)

    avg_news_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

    # Real-time Twitter sentiment
    twitter_sentiment = fetch_twitter_sentiment(ticker)

    return {
        "ticker": ticker,
        "news_sentiment": avg_news_sentiment,
        "social_sentiment": twitter_sentiment,
        "overall_sentiment": (avg_news_sentiment + twitter_sentiment) / 2
    }


def fetch_twitter_sentiment(ticker: str) -> float:
    """
    Fetch recent tweets about the stock and calculate sentiment.
    
    Args:
        ticker (str): The stock ticker symbol.
    
    Returns:
        float: Average sentiment polarity of tweets.
    """
    # query = f"${ticker} -is:retweet lang:en"  # Filter by ticker mention, exclude retweets
    # tweets = client.search_recent_tweets(query=query, max_results=20)
    #
    # sentiments = []
    # if tweets.data:
    #     for tweet in tweets.data:
    #         blob = TextBlob(tweet.text)
    #         sentiments.append(blob.sentiment.polarity)
    #
    # return sum(sentiments) / len(sentiments) if sentiments else 0.0
    return 0.0
