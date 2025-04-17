from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from tools.yf_tech_analysis_tool import yf_tech_analysis
from tools.yf_fundamental_analysis_tool import yf_fundamental_analysis
from tools.sentiment_analysis_tool import sentiment_analysis
from tools.competitor_analysis_tool import competitor_analysis
from tools.risk_assessment_tool import risk_assessment
import os

# Set your Groq API Key
os.environ["GROQ_API_KEY"] = "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"  # Or use dotenv / config management

def create_crew(stock_symbol):
    # Initialize LLaMA-3 from Groq
    llm = ChatGroq(
        model="llama3-8b-8192",  # Or use "llama3-70b-8192" if needed
        temperature=0.2  # Lower temp for financial accuracy
    )

    # Define Agents
    researcher = Agent(
        role='Stock Market Researcher',
        goal='Gather and analyze comprehensive data about the stock',
        backstory="You're an experienced stock market researcher with a keen eye for detail and a talent for uncovering hidden trends.",
        tools=[yf_tech_analysis, yf_fundamental_analysis, competitor_analysis],
        llm=llm
    )

    analyst = Agent(
        role='Financial Analyst',
        goal='Analyze the gathered data and provide investment insights',
        backstory="You're a seasoned financial analyst known for your accurate predictions and ability to synthesize complex information.",
        tools=[yf_tech_analysis, yf_fundamental_analysis, risk_assessment],
        llm=llm
    )

    sentiment_analyst = Agent(
        role='Sentiment Analyst',
        goal='Analyze market sentiment and its potential impact on the stock',
        backstory="You're an expert in behavioral finance and sentiment analysis, capable of gauging market emotions and their effects on stock performance.",
        tools=[sentiment_analysis],
        llm=llm
    )

    strategist = Agent(
        role='Investment Strategist',
        goal='Develop a comprehensive investment strategy based on all available data',
        backstory="You're a renowned investment strategist known for creating tailored investment plans that balance risk and reward.",
        tools=[],
        llm=llm
    )

    # Define Tasks
    research_task = Task(
        description=f"Research {stock_symbol} using advanced technical and fundamental analysis tools. Provide a comprehensive summary of key metrics, including chart patterns, financial ratios, and competitor analysis.",
        agent=researcher
    )

    sentiment_task = Task(
        description=f"Analyze the market sentiment for {stock_symbol} using news and social media data. Evaluate how current sentiment might affect the stock's performance.",
        agent=sentiment_analyst
    )

    analysis_task = Task(
        description=f"Synthesize the research data and sentiment analysis for {stock_symbol}. Conduct a thorough risk assessment and provide a detailed analysis of the stock's potential.",
        agent=analyst
    )

    strategy_task = Task(
        description=f"Based on all the gathered information about {stock_symbol}, develop a comprehensive investment strategy. Consider various scenarios and provide actionable recommendations for different investor profiles.",
        agent=strategist
    )

    # Create Crew
    crew = Crew(
        agents=[researcher, sentiment_analyst, analyst, strategist],
        tasks=[research_task, sentiment_task, analysis_task, strategy_task],
        process=Process.sequential
    )

    return crew

def run_analysis(stock_symbol):
    crew = create_crew(stock_symbol)
    result = crew.kickoff()
    return result
