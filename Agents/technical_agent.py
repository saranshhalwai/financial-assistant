from tools.yf_tech_analysis_tool import yf_tech_analysis
from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY


class TechnicalAgent:
    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol
        self.llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.2
        )

    def generate_signal(self):
        tool_response = yf_tech_analysis(self.stock_symbol)
        prompt = f"""
                You are a financial analyst specialized in technical analysis. Based on the following technical indicators for a stock, analyze the price trends, patterns, and provide an investment recommendation.

                Technical Analysis Data:
                ```
                {tool_response}
                ```

                Generate a JSON response with the following structure:
                {{
                    "trend": "Bullish|Bearish|Neutral",
                    "key_indicators": ["indicator1: interpretation", "indicator2: interpretation", "..."],
                    "support_levels": ["level1", "level2", "..."],
                    "resistance_levels": ["level1", "level2", "..."],
                    "recommendation": "Strong Buy|Buy|Hold|Sell|Strong Sell",
                    "reasoning": "Brief explanation of recommendation based on technical indicators"
                }}

                Only return valid JSON. Do not include markdown, comments, or any explanations. Return JSON only.
                """
        signal = self.llm.invoke(prompt)
        return signal.content


if __name__ == '__main__':
    agent = TechnicalAgent("AAPL")
    signal = agent.generate_signal()
    print(signal)
