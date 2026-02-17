import streamlit as st
import pandas as pd

st.title("Personal Expense Tracker")

# Load Data
df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Show Data
st.header("Transactions")
st.dataframe(df)

# Monthly Spending
expenses = df[df["Amount"] < 0]
monthly = (
    expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"]
    .sum().astype(float)
)

st.header("Monthly Spending")
st.bar_chart(monthly)