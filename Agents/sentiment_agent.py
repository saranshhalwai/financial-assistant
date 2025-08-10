from langchain_groq import ChatGroq

from tools.sentiment_analysis_tool import sentiment_analysis


class SentimentAgent:
    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol
        self.llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.2
        )

    def generate_signal(self):
        tool_response = sentiment_analysis(self.stock_symbol)
        prompt = f"""
                        You are a financial analyst specialized in sentiment analysis. Based on the following sentiment scores for a stock, analyze the market sentiment, news impact, and provide an investment recommendation.

                        Sentiment Analysis Data:
                        ```
                        {tool_response}
                        ```

                        Generate a JSON response with the following structure:
                        {{
                            "market_sentiment": "Positive|Negative|Neutral",
                            "sentiment_indicators": ["news sentiment: interpretation", "social sentiment: interpretation"],
                            "intensity": "Strong|Moderate|Weak",
                            "recommendation": "Strong Buy|Buy|Hold|Sell|Strong Sell",
                            "reasoning": "Brief explanation of recommendation based on sentiment analysis"
                        }}

                        Only return valid JSON. Do not include markdown, comments, or any explanations. Return JSON only.
                        """
        signal = self.llm.invoke(prompt)
        return signal.content


if __name__ == '__main__':
    agent = SentimentAgent("AAPL")
    signal = agent.generate_signal()
    print(signal)
