from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableMap
from langchain_groq import ChatGroq
from langchain.tools import Tool
import os

from tools.yf_tech_analysis_tool import yf_tech_analysis
from tools.yf_fundamental_analysis_tool import yf_fundamental_analysis
from tools.sentiment_analysis_tool import sentiment_analysis
# from tools.competitor_analysis_tool import competitor_analysis
from tools.risk_assessment_tool import risk_assessment

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.2
)

tech_tool = Tool(name="Technical Analysis", func=yf_tech_analysis, description="Performs technical analysis.")
fundamental_tool = Tool(name="Fundamental Analysis", func=yf_fundamental_analysis, description="Performs fundamental analysis.")
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
        "analysis": f"""Tech: {data['technical']}
        Fundamental: {data['fundamental']}
        Competitor: {data.get('competitor', 'N/A')}

        Risk: {risk}"""
    }
# TODO:         Sentiment: {data['sentiment']}

def strategist_chain(analysis: str) -> str:
    prompt = f"Based on the following data, develop a complete investment strategy:\n\n{analysis}"
    return llm.invoke(prompt)

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