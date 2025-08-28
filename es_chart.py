import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np
import sys
from datetime import datetime, timedelta, timezone

st.title('SPY Daily Chart')
st.write('Displaying SPY 1-minute candlestick chart for the previous trading day')

try:
    # Get yesterday's date
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    
    st.info(f"Fetching data for {yesterday}...")

    # Download SPY 1-minute data for yesterday
    data = yf.download("SPY", start=yesterday, end=today, interval="1m", auto_adjust=True)
    
    st.write(f"Raw data shape: {data.shape}")
    st.write(f"Data types: {data.dtypes.to_dict()}")
    
    if data.empty:
        st.warning(f"No data available for {yesterday} (may be weekend/holiday)")
        st.info("Markets are closed on weekends and holidays. Try again on a trading day.")
        st.stop()

    # Filter only yesterday's data
    data = data[data.index.date == yesterday]
    
    if data.empty:
        st.warning(f"No intraday data available for {yesterday}")
        st.stop()
    
    # Create a clean copy with only the columns we need
    data_clean = data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    
    # Convert all data to float64 explicitly
    for col in data_clean.columns:
        data_clean[col] = data_clean[col].astype('float64')
    
    # Reset index to ensure it's proper datetime
    data_clean.index = pd.to_datetime(data_clean.index)
    
    st.success(f"Successfully loaded {len(data_clean)} minutes of trading data")
    st.write(f"Final data types: {data_clean.dtypes.to_dict()}")
    
    # Debug: Show first few rows
    with st.expander("View first 5 rows"):
        st.dataframe(data_clean.head())
    
    # Create the plot
    try:
        fig, axes = mpf.plot(data_clean, 
                           type='candle', 
                           style='charles',
                           title=f"SPY Chart - {yesterday}",
                           volume=True, 
                           mav=(9, 21),
                           returnfig=True,
                           figsize=(12, 8),
                           show_nontrading=False)
        
        # Display the plot in Streamlit
        st.pyplot(fig)
        
    except Exception as plot_error:
        st.error(f"Chart creation failed: {str(plot_error)}")
        st.write("Trying alternative plotting method...")
        
        # Fallback to simple line chart
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
        
        # Price chart
        ax1.plot(data_clean.index, data_clean['Close'], label='Close Price', linewidth=1, color='blue')
        ax1.set_title(f'SPY Chart - {yesterday} (Fallback View)')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True)
        ax1.legend()
        
        # Volume chart
        ax2.bar(data_clean.index, data_clean['Volume'], alpha=0.7, color='orange')
        ax2.set_ylabel('Volume')
        ax2.grid(True)
        
        plt.tight_layout()
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
            st.write(f"pandas version: {pd.__version__}")
        except:
            st.write("Package versions: Not available")
