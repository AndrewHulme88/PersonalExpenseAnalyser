import pandas as pd

df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

monthly_totals = df.groupby("Month")["Amount"].sum().reset_index()
monthly_summary = df.groupby(["Month", "Category"])["Amount"].sum().unstack(fill_value=0)

print(monthly_totals)
print(monthly_summary)
print(df.head())
print(df.info())