import streamlit as st
import pandas as pd

st.title("📊 Hidden Cost of Living in Indian States")

@st.cache_data
def load_data():
    df = pd.read_csv("Expense.csv")
    df.columns = df.columns.str.strip()
    
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=["States/UTs"])
    df["States/UTs"] = df["States/UTs"].astype(str)

    numeric_cols = df.select_dtypes(include='number').columns
    df["Total Expense"] = df[numeric_cols].sum(axis=1)
    df["Food Expense"] = df.drop(columns=["States/UTs", "Rent", "Total Expense"]).sum(axis=1)
    df["Daily Expense"] = df.drop(columns=["States/UTs", "Rent", "Total Expense", "Food Expense"]).sum(axis=1)
    df["Monthly Food+Essentials"] = df["Daily Expense"] * 30
    df["Monthly Rent"] = df["Rent"]
    df["Total Monthly Expense"] = df["Monthly Food+Essentials"] + df["Monthly Rent"]
    df["Required Monthly Income"] = df["Total Monthly Expense"] * 1.25
    df["Required Monthly Income (₹ Thousands)"] = (df["Required Monthly Income"] / 1000).round(2)

    return df
