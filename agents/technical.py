from langchain_core.tools import tool
from pydantic import BaseModel, Field
import pandas as pd
import requests
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, ToolMessage
from config.settings import ALPHA_VANTAGE_API_KEY, GROQ_API_KEY



class CalculateIndicatorsInput(BaseModel):
    indicators: list[str] = Field(description="List of indicators to calculate. Supported: ['SMA_20', 'RSI_14']")


class TechnicalAgent:
    def __init__(self, ticker: str):
        self.df = self.fetch_ohlcv(ticker)
        llm = init_chat_model("llama3-8b-8192", model_provider="groq")
        self.tools = [self.make_indicator_tool()]
        self.llm = llm.bind_tools(self.tools)

    def fetch_ohlcv(self, ticker: str, outputsize='compact'):
        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "outputsize": outputsize,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError(f"Error fetching data: {response.status_code} - {response.text}")
        try:
            ts_data = response.json()["Time Series (Daily)"]
        except KeyError:
            raise ValueError("Invalid response or API limit exceeded.")
        df = pd.DataFrame.from_dict(ts_data, orient="index", dtype=float)
        df = df.rename(columns={
            "1. open": "Open", "2. high": "High", "3. low": "Low",
            "4. close": "Close", "5. adjusted close": "Adj Close",
            "6. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        return df.sort_index()

    def make_indicator_tool(self):
        @tool("calculate_indicators", args_schema=CalculateIndicatorsInput, return_direct=True)
        def _tool(indicators: list[str]):
            """
            Tool to calculate selected technical indicators from OHLCV data.
            Supported indicators: ['SMA_20', 'RSI_14']
            """
            df = self.df
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            if "SMA_20" in indicators:
                df["SMA_20"] = df["Close"].rolling(window=20).mean()

            if "RSI_14" in indicators:
                delta = df['Close'].diff()
                gain = delta.clip(lower=0)
                loss = -delta.clip(upper=0)
                avg_gain = gain.rolling(14).mean()
                avg_loss = loss.rolling(14).mean()
                rs = avg_gain / avg_loss
                df["RSI_14"] = 100 - (100 / (1 + rs))

            return df.round(2).tail(30).to_dict(orient="index")

        return _tool

    def generate_signal(self):
        recent_data = self.df.tail(30).round(2).to_dict(orient="index")

        messages = [
            SystemMessage(content=f"""
            You are a stock market analyst. You are allowed to use the tool `calculate_indicators` if you need to compute technical indicators if needed.
            Here is the last 30 days of OHLCV data:
            {recent_data}
            Provide a trading signal (buy/sell/hold) with a reason.
            Respond in JSON format: {{"signal": "buy|sell|hold", "reason": "your reasoning"}}
            """)
        ]

        response = self.llm.invoke(messages)

        

        while len(response.tool_calls) != 0:
            print("Tool calls detected:")
            print(response.tool_calls)
            tool_args = response.tool_calls[0].get('args')
            tool_result = self.tools[0].invoke(tool_args)
            tool_call_id = response.tool_calls[0]['id']
            tool_message = ToolMessage(content = tool_result, tool_call_id=tool_call_id)
            messages.append(tool_message)
            response = self.llm.invoke(messages)

        print("Final response:")
        print(response.content)

        

def analyze_stock(ticker: str):
    agent = TechnicalAgent(ticker)
    agent.generate_signal()


if __name__ == "__main__":
    analyze_stock("TSLA")
    