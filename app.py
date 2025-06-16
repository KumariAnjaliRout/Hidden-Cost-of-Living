import streamlit as st
import pandas as pd

st.title("📊 Hidden Cost of Living in Indian States")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hidden Cost of Living in Indian States", layout="wide")
st.title("📊 Hidden Cost of Living in Indian States")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Expense.csv")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("CSV is not loaded or is empty. Please upload 'Expense.csv' with correct data.")
else:
    st.success("Data loaded successfully!")
    st.write(df.head())

    option = st.sidebar.selectbox("Choose a Visualization", df.columns[1:].tolist())
    st.write(f"You selected: {option}")


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
