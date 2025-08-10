from langchain_groq import ChatGroq

from tools.yf_fundamental_analysis_tool import yf_fundamental_analysis


class FundamentalAgent:
    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol
        self.llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.2
        )

    def generate_signal(self):
        tool_response = yf_fundamental_analysis(self.stock_symbol)
        prompt = f"""
        You are a financial analyst specialized in fundamental analysis. Based on the following fundamental data for a stock, analyze the company's financial health and provide an investment recommendation.
        
        Fundamental Data:
        ```
        {tool_response}
        ```
        
        Generate a JSON response with the following structure:
        {{
            "financial_health": "Strong|Moderate|Weak",
            "key_strengths": ["strength1", "strength2", "..."],
            "key_concerns": ["concern1", "concern2", "..."],
            "valuation_assessment": "Undervalued|Fair Value|Overvalued",
            "recommendation": "Strong Buy|Buy|Hold|Sell|Strong Sell",
            "reasoning": "Brief explanation of recommendation"
        }}

        Only return valid JSON. Do not include markdown, comments, or any explanations. Return JSON only.
        """
        signal = self.llm.invoke(prompt)
        return signal.content


if __name__ == '__main__':
    agent = FundamentalAgent("AAPL")
    signal = agent.generate_signal()
    print(signal)
