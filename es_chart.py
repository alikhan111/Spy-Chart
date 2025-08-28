import streamlit as st
import sys
from datetime import datetime, timedelta

# Check and install missing packages
try:
    import yfinance as yf
    import mplfinance as mpf
    import matplotlib.pyplot as plt
except ImportError as e:
    st.error(f"Missing required packages: {e}")
    st.info("Please make sure requirements.txt includes: yfinance, mplfinance, matplotlib")
    st.stop()

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
    else:
        # Filter only yesterday's data
        data = data[data.index.date == yesterday]
        
        # Create the plot
        fig, axes = mpf.plot(data, type='candle', style='charles',
                           title=f"SPY Chart - {yesterday}",
                           volume=True, mav=(9, 21),
                           returnfig=True)
        
        # Display the plot in Streamlit
        st.pyplot(fig)
        
        # Show some basic stats
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
    st.info("This might be due to missing data or API issues. Please try again later.")
