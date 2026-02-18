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

# Edit Transaction
st.header("Edit Transaction")

categories = [
    "Food", "Transport", "Shopping", "Bills",
    "Entertainment", "Rent", "Income", "Other"
]

display_df = df.copy()
display_df["Date"] = display_df["Date"].dt.date

row_to_edit = st.selectbox(
    "Select transaction to edit",
    display_df.index,
    format_func=lambda x: f"{display_df.loc[x, 'Date']} | "
                           f"{display_df.loc[x, 'Description']} | "
                           f"{display_df.loc[x, 'Amount']}",
    key="edit_select"
)

selected = df.loc[row_to_edit]

with st.form("edit_form"):
    edit_date = st.date_input("Date", selected["Date"])
    edit_description = st.text_input(
        "Description", selected["Description"]
    )
    edit_amount = st.number_input(
        "Amount", value=float(selected["Amount"]), step=0.01
    )

    edit_category = st.selectbox(
        "Category",
        categories,
        index=categories.index(selected["Category"])
    )

    save_changes = st.form_submit_button("Save Changes")

    if save_changes:
        df.loc[row_to_edit] = [
            pd.to_datetime(edit_date),
            edit_description,
            edit_amount,
            edit_category
        ]

        df.to_csv("transactions.csv", index=False)
        st.success("Transaction updated!")
        st.rerun()

# Delete Transaction
st.header("Delete Transaction")

display_df = df.copy()
display_df["Date"] = display_df["Date"].dt.date

row_to_delete = st.selectbox(
    "Select a transaction to delete",
    display_df.index,
    format_func=lambda x: f"{display_df.loc[x, 'Date']} | "
        f"{display_df.loc[x, 'Description']} | "
        f"{display_df.loc[x, 'Amount']}"
)

if st.button("Delete Selected Transaction"):
    df = df.drop(row_to_delete)
    df.to_csv("transactions.csv", index=False)
    st.success("Transaction deleted!")
    st.rerun()

# Monthly Spending
expenses = df[df["Amount"] < 0]
monthly = (
    expenses.groupby(expenses["Date"].dt.to_period("M"))["Amount"]
    .sum().astype(float)
)

st.header("Monthly Spending")
st.bar_chart(monthly)