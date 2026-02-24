import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Personal Expense Tracker")

# Load Data
df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"], format="mixed")

# Filter Data
st.header("Filters")

# Category Filter
categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.selectbox("Category", categories)

# Month Filter
df["Month"] = df["Date"].dt.to_period("M").astype(str)
months = ["All"] + sorted(df["Month"].unique().tolist())
selected_month = st.selectbox("Month", months)

# Incom toggle
include_income = st.checkbox("Include Income", value=True)

# Apply Filters
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["Month"] == selected_month
    ]

if not include_income:
    filtered_df = filtered_df[
        filtered_df["Amount"] < 0
    ]

# Show Data
st.header("Transactions")
display_df = filtered_df.copy()
display_df["Date"] = display_df["Date"].dt.date
st.dataframe(display_df)

# Input
st.header("Add New Transaction")

with st.form("transaction_form"):
    date = st.date_input("Date")
    description = st.text_input("Description")
    amount = st.number_input("Amount", step=0.01)
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Rent", "Income" "Other"])
    
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
monthly = (
    filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Amount"]
    .sum().reset_index()
)

monthly["Month"] = monthly["Date"].astype(str)
monthly = monthly.sort_values("Date")
y_max = df["Amount"].abs().max() * 1.2

st.header("Monthly Spending")

fig = px.bar(
    monthly,
    x="Month",
    y="Amount",
    title="Monthly Spending",
    text_auto=True
)

fig.update_traces(
    marker_color="#4CAF50",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Net Amount",
    xaxis=dict(type="category"),
    yaxis=dict(range=[-y_max, y_max]),
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)

st.plotly_chart(fig, use_container_width=True)