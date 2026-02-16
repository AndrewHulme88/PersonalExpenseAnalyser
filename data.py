import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

monthly_totals = df.groupby("Month")["Amount"].sum().reset_index()
monthly_summary = df.groupby(["Month", "Category"])["Amount"].sum().unstack(fill_value=0)
expenses = df[df["Amount"] < 0]
monthly_expenses = expenses.groupby("Month")["Amount"].sum()

print(monthly_totals)
print(monthly_summary)
print(monthly_expenses)
print(df.head())
print(df.info())

monthly_expenses.plot(kind="bar", title="Monthly Expenses")
plt.show()