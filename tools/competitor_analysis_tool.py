import yfinance as yf
from langchain.tools import tool
from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY

def generate_etf_ticker_from_groq(industry: str, sector: str, market_cap: int) -> str:
    """
    Call Groq API to get the ETF ticker based on the industry, sector, and market cap.

    Args:
        industry (str): The industry of the stock.
        sector (str): The sector of the stock.
        market_cap (int): The market cap of the stock.

    Returns:
        str: The ETF ticker symbol suggested by Groq.
    """

    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.7,
        api_key=GROQ_API_KEY
    )

    prompt = f"Given a company in the {industry} industry (sector: {sector}) with a market cap of ${market_cap:,}, " \
             "suggest a US ETF ticker that likely holds companies of similar type and scale. " \
             "Respond with just the ETF ticker symbol."

    # Make the request to Groq API
    response = llm.invoke(prompt)
    # Extract ETF ticker from the response
    etf_ticker = response.content.strip().upper()
    return etf_ticker


@tool
def competitor_analysis(ticker: str, num_competitors: int = 3):
    """
    Perform competitor analysis for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        num_competitors (int): Number of top competitors to analyze.

    Returns:
        dict: Competitor analysis results.
    """
    stock = yf.Ticker(ticker)
    info = stock.get_info()
    sector = info.get('sector')
    industry = info.get('industry')
    market_cap = info.get('marketCap')

    etf_ticker = generate_etf_ticker_from_groq(industry, sector, market_cap)

    # Get ETF data and extract competitors
    etf = yf.Ticker(etf_ticker)

    # Handle case where holdings might not be accessible
    holdings = []
    try:
        # Try to get holdings from the ETF info
        if 'holdings' in etf.info and etf.info['holdings']:
            holdings = etf.info['holdings']
        else:
            # If holdings not in info, try to get from holdings method
            holdings_data = etf.holdings
            if holdings_data is not None:
                holdings = [{"symbol": symbol, "holding": percent}
                            for symbol, percent in holdings_data.items()]
    except Exception as e:
        print(f"Error getting holdings for {etf_ticker}: {e}")

    # Get competitors in the same industry
    competitors = [h for h in holdings if h.get('symbol') != ticker][:num_competitors]
    competitor_data = []
    for comp in competitors:
        comp_info = yf.Ticker(comp['symbol']).get_info()
        competitor_data.append({
            "ticker": comp['symbol'],
            "name": comp_info.get('longName'),
            "market_cap": comp_info.get('marketCap'),
            "pe_ratio": comp_info.get('trailingPE'),
            "revenue_growth": comp_info.get('revenueGrowth'),
            "profit_margins": comp_info.get('profitMargins')
        })

    return {
        "main_stock": ticker,
        "industry": industry,
        "sector": sector,
        "market_cap": market_cap,
        "etf_used": etf_ticker,
        "competitors": competitor_data
    }


print(competitor_analysis("AAPL"))
