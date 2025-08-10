# backend/main.py
import json
from typing import Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf

from core import run_analysis

app = FastAPI(title="AI-Powered Advanced Stock Analysis API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    symbol: str


class AnalysisResponse(BaseModel):
    technical_analysis: Optional[Any]
    fundamental_analysis: Optional[Any]
    sentiment_analysis: Optional[Any]
    risk_assessment: Optional[Any]
    competitor_analysis: Optional[Any]
    investment_strategy: Optional[Any]


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: StockRequest):
    try:
        result = run_analysis(request.symbol)
        analysis = json.loads(result)
        return AnalysisResponse(
            technical_analysis=analysis.get("technical_analysis"),
            fundamental_analysis=analysis.get("fundamental_analysis"),
            sentiment_analysis=analysis.get("sentiment_analysis"),
            risk_assessment=analysis.get("risk_assessment"),
            competitor_analysis=analysis.get("competitor_analysis"),
            investment_strategy=analysis.get("investment_strategy"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chart-data/{symbol}")
async def get_chart_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1y")
        return {
            "dates": hist.index.strftime("%Y-%m-%d").tolist(),
            "open": hist["Open"].tolist(),
            "high": hist["High"].tolist(),
            "low": hist["Low"].tolist(),
            "close": hist["Close"].tolist(),
            "volume": hist["Volume"].tolist(),
            "ma50": hist["Close"].rolling(window=50).mean().fillna(0).tolist(),
            "ma200": hist["Close"].rolling(window=200).mean().fillna(0).tolist(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/{symbol}")
async def get_stock_stats(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
