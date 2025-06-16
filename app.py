# app.py
try:
    import streamlit as st
except ModuleNotFoundError:
    raise ImportError("The Streamlit module is not installed. Please run 'pip install streamlit' before executing this app.")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Configuration
st.set_page_config(
    page_title="Hidden Cost of Living in Indian States",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar opens by default
)
st.title(" Hidden Cost of Living in Indian States")
st.markdown("""
This dashboard analyzes the cost of essential commodities and rent across different Indian States and UTs. 

Choose a visualization or analysis below to explore insights.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("Expense.csv")
    df.columns = df.columns.str.strip()
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=["States/UTs"])
    df["States/UTs"] = df["States/UTs"].astype(str)

    # Calculations
    df["Total Expense"] = df.iloc[:, 1:].sum(axis=1)
    df["Food Expense"] = df.drop(columns=["States/UTs", "Rent", "Total Expense"]).sum(axis=1)
    df["Daily Expense"] = df.drop(columns=["States/UTs", "Rent", "Total Expense", "Food Expense"]).sum(axis=1)
    df["Monthly Food+Essentials"] = df["Daily Expense"] * 30
    df["Monthly Rent"] = df["Rent"]
    df["Total Monthly Expense"] = df["Monthly Food+Essentials"] + df["Monthly Rent"]
    df["Required Monthly Income"] = df["Total Monthly Expense"] * 1.25
    df["Required Monthly Income (₹ Thousands)"] = (df["Required Monthly Income"] / 1000).round(2)

    return df

df = load_data()
df_sorted = df.sort_values(by="Total Expense", ascending=False).reset_index(drop=True)

# Sidebar options
option = st.sidebar.selectbox("Choose a Visualization", [
    "Top 10 Expensive States",
    "Bottom 10 Cheapest States",
    "Food vs Rent Distribution",
    "States by Food Expense",
    "States by Rent",
    "Required Monthly Income"
])

# Visualization
if option == "Top 10 Expensive States":
    top10 = df_sorted.head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Total Expense", y="States/UTs", data=top10, palette="Reds_r", ax=ax)
    ax.set_title("Top 10 Most Expensive States (Total Expense)")
    st.pyplot(fig)

elif option == "Bottom 10 Cheapest States":
    bottom10 = df_sorted.tail(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Total Expense", y="States/UTs", data=bottom10, palette="Greens", ax=ax)
    ax.set_title("Top 10 Least Expensive States (Total Expense)")
    st.pyplot(fig)

elif option == "Food vs Rent Distribution":
    total_food = df["Food Expense"].sum()
    total_rent = df["Rent"].sum()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([total_food, total_rent], labels=["Food", "Rent"], colors=['#f4a261','#2a9d8f'],
           autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
    ax.set_title("Expense Distribution: Food vs. Rent")
    st.pyplot(fig)

elif option == "States by Food Expense":
    df_food_sorted = df.sort_values(by="Food Expense", ascending=False)
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.barh(df_food_sorted['States/UTs'], df_food_sorted['Food Expense'], color='teal')
    ax.set_title("States Ranked by Food Expense")
    ax.set_xlabel("Food Expense (₹)")
    ax.invert_yaxis()
    st.pyplot(fig)

elif option == "States by Rent":
    df_rent_sorted = df.sort_values(by="Rent", ascending=False)
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.barh(df_rent_sorted['States/UTs'], df_rent_sorted['Rent'], color='salmon')
    ax.set_title("States Ranked by Rent Expense")
    ax.set_xlabel("Rent (₹)")
    ax.invert_yaxis()
    st.pyplot(fig)

elif option == "Required Monthly Income":
    df_income_sorted = df.sort_values(by="Required Monthly Income", ascending=False)
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.barplot(
        data=df_income_sorted,
        x="Required Monthly Income (₹ Thousands)",
        y="States/UTs",
        palette="magma",
        ax=ax
    )
    ax.set_title("Required Monthly Income to Live Comfortably in Each State (₹ Thousands)")
    ax.set_xlabel("Monthly Income (₹ Thousands)")
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    st.pyplot(fig)

# Data Table
with st.expander("View Raw Data"):
    st.dataframe(df_sorted)
