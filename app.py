import streamlit as st
import pandas as pd

st.title("📊 Hidden Cost of Living in Indian States")

@st.cache_data
def load_data():
    df = pd.read_csv("Expense.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.dataframe(df)
df["Total Expense"] = df.iloc[:, 1:].sum(axis=1)
df["Food Expense"] = df.drop(columns=["States/UTs", "Rent", "Total Expense"]).sum(axis=1)
df["Required Monthly Income"] = (df["Total Expense"] * 1.25).round(2)

st.write(df[["States/UTs", "Total Expense", "Food Expense", "Required Monthly Income"]])
import matplotlib.pyplot as plt
import seaborn as sns

top10 = df.sort_values(by="Total Expense", ascending=False).head(10)
fig, ax = plt.subplots()
sns.barplot(x="Total Expense", y="States/UTs", data=top10, ax=ax)
st.pyplot(fig)
