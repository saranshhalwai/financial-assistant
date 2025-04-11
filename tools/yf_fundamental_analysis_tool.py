import yfinance as yf
from crewai_tools import tool

@tool
def yf_fundamental_analysis(ticker: str):
    """
    Perform comprehensive fundamental analysis on a given stock ticker.
    
    Args:
        ticker (str): The stock ticker symbol.
    
    Returns:
        dict: Comprehensive fundamental analysis results.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    
    # Calculate additional financial ratios
    try:
        current_ratio = balance_sheet.loc['Total Current Assets'].iloc[-1] / balance_sheet.loc['Total Current Liabilities'].iloc[-1]
        debt_to_equity = balance_sheet.loc['Total Liabilities'].iloc[-1] / balance_sheet.loc['Total Stockholder Equity'].iloc[-1]
        roe = financials.loc['Net Income'].iloc[-1] / balance_sheet.loc['Total Stockholder Equity'].iloc[-1]
        roa = financials.loc['Net Income'].iloc[-1] / balance_sheet.loc['Total Assets'].iloc[-1]
        
        # Calculate growth rates
        revenue_growth = (financials.loc['Total Revenue'].iloc[-1] - financials.loc['Total Revenue'].iloc[-2]) / financials.loc['Total Revenue'].iloc[-2]
        net_income_growth = (financials.loc['Net Income'].iloc[-1] - financials.loc['Net Income'].iloc[-2]) / financials.loc['Net Income'].iloc[-2]
        
        # Free Cash Flow calculation
        fcf = cash_flow.loc['Operating Cash Flow'].iloc[-1] - cash_flow.loc['Capital Expenditures'].iloc[-1]
    except:
        current_ratio = debt_to_equity = roe = roa = revenue_growth = net_income_growth = fcf = None
    
    return {
        "ticker": ticker,
        "company_name": info.get('longName'),
        "sector": info.get('sector'),
        "industry": info.get('industry'),
        "market_cap": info.get('marketCap'),
        "pe_ratio": info.get('trailingPE'),
        "forward_pe": info.get('forwardPE'),
        "peg_ratio": info.get('pegRatio'),
        "price_to_book": info.get('priceToBook'),
        "dividend_yield": info.get('dividendYield'),
        "beta": info.get('beta'),
        "52_week_high": info.get('fiftyTwoWeekHigh'),
        "52_week_low": info.get('fiftyTwoWeekLow'),
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity,
        "return_on_equity": roe,
        "return_on_assets": roa,
        "revenue_growth": revenue_growth,
        "net_income_growth": net_income_growth,
        "free_cash_flow": fcf,
        "analyst_recommendation": info.get('recommendationKey'),
        "target_price": info.get('targetMeanPrice')
    }
