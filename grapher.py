from prophet import Prophet
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def prophet_forecast(ticker: str, period: str = "1y"):
    # Fetch data
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    # Prepare the data for Prophet
    df = history[['Close']].reset_index()
    df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)

    # Remove timezone information from 'ds' column if present
    df['ds'] = df['ds'].dt.tz_localize(None)  # This removes the timezone

    # Initialize Prophet model
    model = Prophet()
    model.fit(df)

    
    future = model.make_future_dataframe(periods=30)  # Predict for the next year
    forecast = model.predict(future)

    # Plot forecast
    model.plot(forecast)
    plt.title(f'Prophet Forecast for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

if __name__ == "__main__":
    ticker = "AAPL"
    period = "1y"
    prophet_forecast(ticker, period)
