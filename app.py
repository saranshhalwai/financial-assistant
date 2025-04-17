import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from crew import run_analysis
import json

def main():
    st.set_page_config(layout="wide")
    st.title("AI-Powered Advanced Stock Analysis")

    # User input
    stock_symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")
    
    if st.button("Analyze Stock"):
        # Run CrewAI analysis
        with st.spinner("Performing comprehensive stock analysis..."):
            result = run_analysis(stock_symbol)
        
        # Parse the result
        analysis = json.loads(result)
        
        # Display analysis result
        st.header("AI Analysis Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Technical Analysis")
            st.write(analysis.get('technical_analysis', 'No technical analysis available'))
            
            st.subheader("Chart Patterns")
            st.write(analysis.get('chart_patterns', 'No chart patterns identified'))
        
        with col2:
            st.subheader("Fundamental Analysis")
            st.write(analysis.get('fundamental_analysis', 'No fundamental analysis available'))
            
            st.subheader("Sentiment Analysis")
            st.write(analysis.get('sentiment_analysis', 'No sentiment analysis available'))
        
        st.subheader("Risk Assessment")
        st.write(analysis.get('risk_assessment', 'No risk assessment available'))
        
        st.subheader("Competitor Analysis")
        st.write(analysis.get('competitor_analysis', 'No competitor analysis available'))
        
        st.subheader("Investment Strategy")
        st.write(analysis.get('investment_strategy', 'No investment strategy available'))
        
        # Fetch stock data for chart
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="1y")
        
        # Create interactive chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=hist.index,
                                     open=hist['Open'],
                                     high=hist['High'],
                                     low=hist['Low'],
                                     close=hist['Close'],
                                     name='Price'))
        
        # Add volume bars
        fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', yaxis='y2'))
        
        # Add moving averages
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(window=50).mean(), name='50-day MA'))
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(window=200).mean(), name='200-day MA'))
        
        fig.update_layout(
            title=f"{stock_symbol} Stock Analysis",
            yaxis_title='Price',
            yaxis2=dict(title='Volume', overlaying='y', side='right'),
            xaxis_rangeslider_visible=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display key statistics
        st.subheader("Key Statistics")
        info = stock.info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}")
            st.metric("P/E Ratio", round(info.get('trailingPE', 0), 2))
        with col2:
            st.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 0):,.2f}")
            st.metric("52 Week Low", f"${info.get('fiftyTwoWeekLow', 0):,.2f}")
        with col3:
            st.metric("Dividend Yield", f"{info.get('dividendYield', 0):.2%}")
            st.metric("Beta", round(info.get('beta', 0), 2))

if __name__ == "__main__":
    main()
