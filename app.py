import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
df = pd.read_csv("Expense.csv")

# Convert numeric columns
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Total Expense Calculation
df["Total Expense"] = df.iloc[:, 1:].sum(axis=1)
df_sorted = df.sort_values(by="Total Expense", ascending=False).reset_index(drop=True)

# Save updated CSV
df_sorted.to_csv("total_expense_with_rent.csv", index=False)

# Summary Stats
print("Average Total Expense: ₹", df["Total Expense"].mean())
print("Maximum Expense: ₹", df["Total Expense"].max())
print("Minimum Expense: ₹", df["Total Expense"].min())

# Heatmap of all commodities
plt.figure(figsize=(15, 10))
sns.heatmap(df.set_index("States/UTs").iloc[:, :-2], cmap="plasma")
plt.title("Essential Commodity Prices by State", fontsize=16)
plt.xlabel("Commodities", fontsize=12)
plt.ylabel("States/UTs", fontsize=12)
plt.tight_layout()
plt.show()

# Top 10 Expensive States
top10 = df_sorted.head(10)
plt.figure(figsize=(12, 7))
sns.barplot(x="Total Expense", y="States/UTs", data=top10, palette="Reds_r")
plt.title("Top 10 Most Expensive States (Total Expense)")
plt.tight_layout()
plt.show()

# Bottom 10 Cheapest States
bottom10 = df_sorted.tail(10)
plt.figure(figsize=(12, 7))
sns.barplot(x="Total Expense", y="States/UTs", data=bottom10, palette="Greens")
plt.title("Top 10 Least Expensive States (Total Expense)")
plt.tight_layout()
plt.show()

# Pie Chart: Food vs. Rent
# Strip column names of leading/trailing spaces
df.columns = df.columns.str.strip()

# Now drop safely
total_food = df.drop(columns=["States/UTs", "Rent", "Total Expense"]).sum().sum()

total_rent = df["Rent"].sum()

plt.figure(figsize=(7, 7))
plt.pie([total_food, total_rent], labels=["Food", "Rent"], colors=['#f4a261','#2a9d8f'],
        autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
plt.title("Expense Distribution: Food vs. Rent")
plt.axis('equal')
plt.tight_layout()
plt.show()

# Rank States by Food Expense
df["Food Expense"] = df.drop(columns=["States/UTs", "Rent", "Total Expense"]).sum(axis=1)
plt.figure(figsize=(14, 8))
plt.barh(df_sorted['States/UTs'], df_sorted['Food Expense'], color='teal')
plt.xlabel('Total Food Expense (₹)')
plt.ylabel('States/UTs')
plt.title('States Ranked by Food Expense')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Rank States by Rent
df_rent_sorted = df.sort_values(by="Rent", ascending=False)
plt.figure(figsize=(14, 8))
plt.barh(df_rent_sorted['States/UTs'], df_rent_sorted['Rent'], color='salmon')
plt.xlabel('Rent (₹)')
plt.ylabel('States/UTs')
plt.title('States Ranked by Rent Expense')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Monthly & Annual Income Estimation
food_columns = df.columns.difference(['States/UTs', 'Rent'])
df["Daily Expense"] = df[food_columns].sum(axis=1)
df["Monthly Food+Essentials"] = df["Daily Expense"] * 30
df["Monthly Rent"] = df["Rent"]
df["Total Monthly Expense"] = df["Monthly Food+Essentials"] + df["Monthly Rent"]
df["Required Monthly Income"] = df["Total Monthly Expense"] * 1.25
df["Required Monthly Income (₹ Thousands)"] = (df["Required Monthly Income"] / 1e3).round(2)

# Plot Required Monthly Income
plt.figure(figsize=(15, 12))
sns.barplot(
    data=df.sort_values("Required Monthly Income", ascending=False),
    x="Required Monthly Income (₹ Thousands)",
    y="States/UTs",
    palette="magma"
)
plt.title("Required Monthly Income to Live Comfortably in Each State (in ₹ Thousands)", fontsize=14)
plt.xlabel("Monthly Income (₹ Thousands)")
plt.ylabel("States/UTs")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
