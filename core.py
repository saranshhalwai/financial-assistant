import os

from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_groq import ChatGroq

# from tools.competitor_analysis_tool import competitor_analysis
from tools.risk_assessment_tool import risk_assessment
from Agents.fundamental_agent import FundamentalAgent
from Agents.technical_agent import TechnicalAgent
from Agents.sentiment_agent import SentimentAgent
load_dotenv()


llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.2
)


risk_tool = Tool(name="Risk Assessment", func=risk_assessment, description="Assesses risk.")


def researcher_chain(stock_symbol: str) -> dict:
    return {
        "technical": TechnicalAgent(stock_symbol).generate_signal(),
        "fundamental": FundamentalAgent(stock_symbol).generate_signal(),
        # "competitor": competitor_analysis(stock_symbol)
    }


def sentiment_chain(stock_symbol: str) -> dict:
    return {
        "sentiment": SentimentAgent(stock_symbol).generate_signal()
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
