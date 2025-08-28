import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.title('SPY Daily Chart')
st.write('Displaying SPY 1-minute candlestick chart for the previous trading day')

try:
    # Get yesterday's date
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    # Download SPY 1-minute data for yesterday
    data = yf.download("SPY", start=yesterday, end=today, interval="1m")
    
    if data.empty:
        st.warning(f"No data available for {yesterday} (may be weekend/holiday)")
        st.info("Markets are closed on weekends and holidays. Try again on a trading day.")
        st.stop()

    # Filter only yesterday's data
    data = data[data.index.date == yesterday]
    
    if data.empty:
        st.warning(f"No intraday data available for {yesterday}")
        st.stop()
    
    # Clean the data
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    data_clean = data.dropna(subset=['Open', 'High', 'Low', 'Close'])
    
    if data_clean.empty:
        st.error("No valid data after cleaning. Please try again later.")
        st.stop()
    
    # Create the plot
    fig, axes = mpf.plot(data_clean, type='candle', style='charles',
                       title=f"SPY Chart - {yesterday}",
                       volume=True, 
                       mav=(9, 21),
                       returnfig=True)
    
    st.pyplot(fig)
    
    # Show statistics
    st.subheader('Daily Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open", f"${data_clean['Open'].iloc[0]:.2f}")
    with col2:
        st.metric("Close", f"${data_clean['Close'].iloc[-1]:.2f}")
    with col3:
        change = data_clean['Close'].iloc[-1] - data_clean['Open'].iloc[0]
        change_pct = (change / data_clean['Open'].iloc[0]) * 100
        st.metric("Change", f"${change:.2f}", f"{change_pct:.2f}%")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please try again later or check if markets were open yesterday.")
