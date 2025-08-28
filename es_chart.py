import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

st.title('SPY Daily Chart')
st.write('Displaying SPY 1-minute chart for the previous trading day')

try:
    # Get yesterday's date
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    
    st.info(f"Fetching data for {yesterday}...")

    # Download SPY data
    data = yf.download("SPY", start=yesterday, end=today, interval="1m", auto_adjust=True)
    
    if data.empty:
        st.warning(f"No data available for {yesterday}")
        st.stop()

    data = data[data.index.date == yesterday]
    
    if data.empty:
        st.warning(f"No intraday data for {yesterday}")
        st.stop()
    
    # Convert to numeric
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    data = data.dropna()
    
    # Create OHLC chart manually
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    # OHLC bars
    for i, (idx, row) in enumerate(data.iterrows()):
        ax1.plot([i, i], [row['Low'], row['High']], color='black', linewidth=1)
        ax1.plot([i, i], [row['Open'], row['Close']], color='green' if row['Close'] >= row['Open'] else 'red', linewidth=3)
    
    ax1.set_title(f'SPY OHLC Chart - {yesterday}')
    ax1.set_ylabel('Price ($)')
    ax1.grid(True)
    
    # Volume chart
    ax2.bar(range(len(data)), data['Volume'], alpha=0.7, color='blue')
    ax2.set_ylabel('Volume')
    ax2.grid(True)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Show statistics
    st.subheader('Daily Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open", f"${data['Open'].iloc[0]:.2f}")
    with col2:
        st.metric("Close", f"${data['Close'].iloc[-1]:.2f}")
    with col3:
        change = data['Close'].iloc[-1] - data['Open'].iloc[0]
        change_pct = (change / data['Open'].iloc[0]) * 100
        st.metric("Change", f"${change:.2f}", f"{change_pct:.2f}%")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
