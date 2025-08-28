import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np
import sys
from datetime import datetime, timedelta

st.title('SPY Daily Chart')
st.write('Displaying SPY 1-minute candlestick chart for the previous trading day')

try:
    # Get yesterday's date
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    st.info(f"Fetching data for {yesterday}...")

    # Download SPY 1-minute data for yesterday
    data = yf.download("SPY", start=yesterday, end=today, interval="1m")
    
    # Debug: Show raw data info
    st.write(f"Raw data shape: {data.shape}")
    
    if data.empty:
        st.warning(f"No data available for {yesterday} (may be weekend/holiday)")
        st.info("Markets are closed on weekends and holidays. Try again on a trading day.")
        st.stop()

    # Filter only yesterday's data
    data = data[data.index.date == yesterday]
    
    if data.empty:
        st.warning(f"No intraday data available for {yesterday}")
        st.stop()
    
    # Clean the data - convert all numeric columns to float and handle NaN values
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    for col in numeric_columns:
        if col in data.columns:
            # Convert to numeric, coercing errors to NaN
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Drop any rows with NaN values in essential columns
    data_clean = data.dropna(subset=['Open', 'High', 'Low', 'Close'])
    
    if data_clean.empty:
        st.error("No valid data after cleaning. Please try again later.")
        st.stop()
    
    st.success(f"Successfully loaded {len(data_clean)} minutes of trading data")
    
    # Create the plot
    fig, axes = mpf.plot(data_clean, type='candle', style='charles',
                       title=f"SPY Chart - {yesterday}",
                       volume=True, 
                       mav=(9, 21),
                       returnfig=True,
                       figsize=(12, 8))
    
    # Display the plot in Streamlit
    st.pyplot(fig)
    
    # Show some basic stats
    st.subheader('Daily Statistics')
    
    if not data_clean.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Open", f"${data_clean['Open'].iloc[0]:.2f}")
        with col2:
            st.metric("Close", f"${data_clean['Close'].iloc[-1]:.2f}")
        with col3:
            change = data_clean['Close'].iloc[-1] - data_clean['Open'].iloc[0]
            st.metric("Net Change", f"${change:.2f}")
        with col4:
            change_pct = (change / data_clean['Open'].iloc[0]) * 100
            st.metric("% Change", f"{change_pct:.2f}%")
        
        # Additional stats
        st.subheader('Session Details')
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("High", f"${data_clean['High'].max():.2f}")
        with col6:
            st.metric("Low", f"${data_clean['Low'].min():.2f}")
        with col7:
            st.metric("Volume", f"{data_clean['Volume'].sum():,}")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("This might be due to missing data or API issues. Please try again later.")
    
    # Debug info
    with st.expander("Technical Details (for debugging)"):
        st.write(f"Error type: {type(e).__name__}")
        st.write(f"Python version: {sys.version}")
        try:
            st.write(f"yfinance version: {yf.__version__}")
        except:
            st.write("yfinance version: Not available")
