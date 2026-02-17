import streamlit as st
import pandas as pd

st.title("Personal Expense Tracker")

# Load Data
df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"], format="mixed")

# Show Data
st.header("Transactions")
display_df = df.copy()
display_df["Date"] = display_df["Date"].dt.date
st.dataframe(display_df)

# Input
st.header("Add New Transaction")

with st.form("transaction_form"):
    date = st.date_input("Date")
    description = st.text_input("Description")
    amount = st.number_input("Amount", step=0.01)
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Rent", "Other"])
    
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        new_row = pd.DataFrame([{
            "Date": pd.to_datetime(date),
            "Description": description,
            "Amount": amount,
            "Category": category
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("transactions.csv", index=False)

        st.success("Transaction added! Refreshing...")
        st.rerun()

# Monthly Spending
expenses = df[df["Amount"] < 0]
monthly = (
    expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"]
    .sum().astype(float)
)

st.header("Monthly Spending")
st.bar_chart(monthly)