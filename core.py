import os

from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_groq import ChatGroq

# from tools.competitor_analysis_tool import competitor_analysis
from tools.risk_assessment_tool import risk_assessment
from tools.sentiment_analysis_tool import sentiment_analysis
from tools.yf_fundamental_analysis_tool import yf_fundamental_analysis
from tools.yf_tech_analysis_tool import yf_tech_analysis

load_dotenv()
os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.2
)

tech_tool = Tool(name="Technical Analysis", func=yf_tech_analysis, description="Performs technical analysis.")
fundamental_tool = Tool(name="Fundamental Analysis", func=yf_fundamental_analysis,
                        description="Performs fundamental analysis.")
# competitor_tool = Tool(name="Competitor Analysis", func=competitor_analysis, description="Analyzes competitors.")
sentiment_tool = Tool(name="Sentiment Analysis", func=sentiment_analysis, description="Analyzes market sentiment.")
risk_tool = Tool(name="Risk Assessment", func=risk_assessment, description="Assesses risk.")


def researcher_chain(stock_symbol: str) -> dict:
    return {
        "technical": yf_tech_analysis(stock_symbol),
        "fundamental": yf_fundamental_analysis(stock_symbol),
        # "competitor": competitor_analysis(stock_symbol)
    }


def sentiment_chain(stock_symbol: str) -> dict:
    return {
        "sentiment": sentiment_analysis(stock_symbol)
    }


def analyst_chain(data: dict) -> dict:
    stock_symbol = data["symbol"]
    risk = risk_assessment(stock_symbol)
    return {
        "analysis": f"""Technical Analysis: {data['technical']}
        Fundamental Analysis: {data['fundamental']}
        Sentiment Analysis: {data['sentiment']}
        Risk Assessment: {risk}"""
    }


def strategist_chain(analysis: str) -> str:
    prompt = f"""
    You are a financial analyst assistant. You have been provided this data. Your job is to conduct the analysis and respond after thinking. Based on the following data, output a JSON with these fields:
    
    - technical_analysis
    - fundamental_analysis
    - sentiment_analysis
    - risk_assessment
    - investment_strategy
    
    Only return valid JSON. Do not include markdown, comments, or any explanations. Return JSON only.
    
    Analysis:
    {analysis}
    """
    response = llm.invoke(prompt).content
    print(response)
    return response  # Ensure this returns a JSON string


# LangChain pipeline
def run_analysis(stock_symbol: str) -> str:
    research = researcher_chain(stock_symbol)
    sentiment = sentiment_chain(stock_symbol)

    combined_data = {
        "symbol": stock_symbol,
        "technical": research["technical"],
        "fundamental": research["fundamental"],
        # "competitor": research["competitor"],
        "sentiment": sentiment["sentiment"]
    }

    analysis = analyst_chain(combined_data)
    strategy = strategist_chain(analysis["analysis"])

    return strategy


if __name__ == "__main__":
    print(run_analysis("AAPL"))
