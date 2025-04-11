import yfinance as yf
import numpy as np
from scipy import stats
from crewai_tools import tool

@tool
def risk_assessment(ticker: str, benchmark: str = "^GSPC", period: str = "5y"):
    """
    Perform risk assessment for a given stock.
    
    Args:
        ticker (str): The stock ticker symbol.
        benchmark (str): Benchmark index for comparison (default: S&P 500).
        period (str): Time period for analysis.
    
    Returns:
        dict: Risk assessment results.
    """
    stock = yf.Ticker(ticker)
    benchmark_index = yf.Ticker(benchmark)
    
    stock_data = stock.history(period=period)['Close']
    benchmark_data = benchmark_index.history(period=period)['Close']
    
    # Calculate returns
    stock_returns = stock_data.pct_change().dropna()
    benchmark_returns = benchmark_data.pct_change().dropna()
    
    # Calculate beta
    covariance = np.cov(stock_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    beta = covariance / benchmark_variance
    
    # Calculate Sharpe ratio
    risk_free_rate = 0.02  # Assume 2% risk-free rate
    excess_returns = stock_returns - risk_free_rate
    sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    
    # Calculate Value at Risk (VaR)
    var_95 = np.percentile(stock_returns, 5)
    
    # Calculate Maximum Drawdown
    cumulative_returns = (1 + stock_returns).cumprod()
    max_drawdown = (cumulative_returns.cummax() - cumulative_returns).max()
    
    return {
        "ticker": ticker,
        "beta": beta,
        "sharpe_ratio": sharpe_ratio,
        "value_at_risk_95": var_95,
        "max_drawdown": max_drawdown,
        "volatility": stock_returns.std() * np.sqrt(252)
    }
