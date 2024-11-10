import streamlit as st
import numpy as np
from scipy.stats import norm
import pandas as pd

st.title("Black-Scholes-Merton Calculator")

#parameters

st.sidebar.write("## Input Data")

S = st.sidebar.number_input("Underlying Price", min_value = 0.0, value = 100.0)
K = st.sidebar.number_input("Strike Price", min_value = 0.0, value = 110.0)
r = st.sidebar.number_input("Risk-Free-Rate p.a.", value = 0.03)
t = st.sidebar.number_input("Number of days until expiration", min_value = 0.0, value = 245.0)
t = t/365.25
q = st.sidebar.number_input("Dividend Yield p.a.", min_value = 0.0, value = 0.05)
vol = st.sidebar.slider("Volatilité p.a.", min_value = 0.0, value = 0.3, max_value=1.0)




#d1 and d2 computation

d1 = ( np.log(S/K) + t*( r-q+ (vol**2)/2 ) ) / ( vol*np.sqrt(t) )
d2 = d1 - vol*np.sqrt(t)

#Put and Call Premiums

Call_Premium = S*np.exp(-q*t)*norm.cdf(d1, 0, 1) - K*np.exp(-r*t)*norm.cdf(d2, 0, 1)
Put_Premium = K*np.exp(-r*t)*norm.cdf(-d2) - S*np.exp(-q*t)*norm.cdf(-d1)

# display option premiums with styling for the text boxes

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="
            padding: 5px; 
            background-color: #68BD43; 
            border-radius: 5px; 
            text-align: center; 
            width: 100%;">
            <h3 style="margin: 0;">CALL Value</h3>
            <p style="margin: 0; font-size: 24px; color: #000000; font-weight: bold;">${round(Call_Premium, 4):.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="
            padding: 5px; 
            background-color: #E49392; 
            border-radius: 5px; 
            text-align: center; 
            width: 100%;">
            <h3 style="margin: 0;">PUT Value</h3>
            <p style="margin: 0; font-size: 24px; color: #000000; font-weight: bold;">${round(Put_Premium, 4):.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Creating a range of underlying prices centered around input S, ensuring non-negative values
lower_bound = max(0, K - 30)  # Ensure non-negative lower bound
upper_bound = K + 30
underlying_prices = np.linspace(lower_bound, upper_bound, 50)

# Calculating Call Option and Put Option Net Profit (including premium)
net_profits_call_long = []
net_profits_call_short = []
net_profits_put_long = []
net_profits_put_short = []
for underlying in underlying_prices:
    # Long Call Option Calculations
    Call_Payoff_long = max(0, underlying - K)  # Long Call option payoff (ignores premium)
    Net_Profit_Call_long = Call_Payoff_long - Call_Premium  # Net profit for Long call option
    net_profits_call_long.append(Net_Profit_Call_long)

      # Short Call Option Calculations
    Call_Payoff_short = - max(0, underlying - K)  # Short Call option payoff (ignores premium)
    Net_Profit_Call_short = Call_Payoff_short + Call_Premium  # Net profit for Short call option
    net_profits_call_short.append(Net_Profit_Call_short)
    
    # Long Put Option Calculations
    Put_Payoff_long = max(0, K - underlying)  #long Put option payoff
    Net_Profit_Put_long = Put_Payoff_long - Put_Premium  # Net profit for long put option
    net_profits_put_long.append(Net_Profit_Put_long)

    # Short Put Option Calculations
    Put_Payoff_short = - max(0, K - underlying)  # short Put option payoff
    Net_Profit_Put_short = Put_Payoff_short + Put_Premium  # Net profit for short put option
    net_profits_put_short.append(Net_Profit_Put_short)

# x axis choises
st.write("")
st.write("")
st.write("")
selected_options = st.multiselect(
    "Choose what you want to display:",
    options=["Long Call", "Short Call", "Long Put", "Short Put"],
    default=["Long Call", "Short Call", "Long Put", "Short Put"]
)
st.write("")
st.write("")
st.write("")

# Base DataFrame with the underlying price column
df_dict = {
    'Underlying Price': underlying_prices,
}

# Conditionally add data based on selected options (using a dictionary)
if "Long Call" in selected_options:
    df_dict['Long Call'] = net_profits_call_long
if "Short Call" in selected_options:
    df_dict['Short Call'] = net_profits_call_short
if "Long Put" in selected_options:
    df_dict['Long Put'] = net_profits_put_long
if "Short Put" in selected_options:
    df_dict['Short Put'] = net_profits_put_short

# Create the DataFrame
df = pd.DataFrame(df_dict)

# Determine which columns should be plotted (only those present in the DataFrame)
columns_to_plot = [col for col in ['Long Call', 'Short Call', 'Long Put', 'Short Put'] if col in df.columns]

# Plot using Streamlit's st.line_chart() if there are columns to plot
if columns_to_plot:
    st.line_chart(
        data=df,
        x='Underlying Price',
        y=columns_to_plot,
        x_label='Underlying Price at Maturity',
        y_label="Option's Payoff"
    )
else:
    st.write("No options selected to display in the plot.")









#to open the website "streamlit run main.py"