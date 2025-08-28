import streamlit as st
import yfinance as yf
import mplfinance as mpf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.title('SPY Daily Chart')
st.write('Displaying SPY 1-minute candlestick chart for the previous trading day')

try:
    # Get yesterday's date
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    # Download SPY 1-minute data for yesterday
    data = yf.download("SPY", start=yesterday, end=today, interval="1m")

    # Filter only yesterday's data
    data = data[data.index.date == yesterday]

    if data.empty:
        st.warning(f"No data available for {yesterday}")
    else:
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
            st.metric("Change", f"${change:.2f}")

except ImportError as e:
    st.error("Required packages not installed. Please check your requirements.txt file")
    st.code("pip install yfinance mplfinance")
except Exception as e:
    st.error(f"An error occurred: {e}")
