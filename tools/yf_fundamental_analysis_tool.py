import yfinance as yf
from langchain.tools import tool


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
    financials = stock.financials.T
    balance_sheet = stock.balance_sheet.T
    cash_flow = stock.cashflow.T

    # Calculate additional financial ratios
    try:
        current_ratio = balance_sheet['Current Assets'].iloc[0] / balance_sheet['Current Liabilities'].iloc[0]
        debt_to_equity = balance_sheet['Total Liabilities Net Minority Interest'].iloc[0] / \
                         balance_sheet['Stockholders Equity'].iloc[0]
        roe = financials['Net Income'].iloc[0] / balance_sheet['Stockholders Equity'].iloc[0]
        roa = financials['Net Income'].iloc[0] / balance_sheet['Total Assets'].iloc[0]

        # Calculate growth rates
        revenue_growth = (financials['Total Revenue'].iloc[0] - financials['Total Revenue'].iloc[1]) / \
                         financials['Total Revenue'].iloc[1]
        net_income_growth = (financials['Net Income'].iloc[0] - financials['Net Income'].iloc[1]) / \
                            financials['Net Income'].iloc[1]

        # Free Cash Flow calculation
        fcf = cash_flow['Operating Cash Flow'].iloc[0] - cash_flow['Capital Expenditure'].iloc[0]
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
