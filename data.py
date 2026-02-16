import pandas as pd

df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

monthly_expenses = df.groupby("Month")["Amount"].sum().reset_index()

print(monthly_expenses)
print(df.head())
print(df.info())