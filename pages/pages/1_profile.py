import streamlit as st
import pandas as pd

st.write("# project2")

#text basics

st.title("This is my page title !")
st.header("This is a header")
st.subheader("This is a subheader")
st.markdown("This is regular text")
st.write("this is also regular text")

st.write("this is text 1")
st.markdown("---")
st.write("this is texte 2")

st.write("# Hello 1")
st.write("## Hello 2")
st.write("### Hello 3")


with st.expander("Click here to see the Apple stock price"):
    st.write("Here it is:")
    st.metric(label = "Apple", value = "$69", delta = "$4")

st.button("Buy 1 APPL stock")
st.multiselect("Choose your city:", options=["Paris", "Nice", "Bordeaux"])


# Create data to represent the line x = 2
x_values = [2, 2]  # Constant x values for a vertical line
y_values = [0, 10]  # Range of y values to visualize the line (you can adjust this range)

# Create a DataFrame
df = pd.DataFrame({
    'x': x_values,
    'y': y_values
})

# Plot using Streamlit's line chart
st.line_chart(data=df, x='x', y='y')


