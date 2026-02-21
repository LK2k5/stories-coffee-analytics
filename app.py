import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stories Coffee Analytics", layout="wide")

st.title("☕ Stories Coffee – Analytics Dashboard")

st.markdown("""
This dashboard shows key insights from cleaned sales data:
- Monthly sales trends  
- Branch performance  
- Category summary (Food vs Beverage)
""")

# Load cleaned data
try:
    monthly = pd.read_csv("clean_monthly_sales_file1.csv")
    category = pd.read_csv("clean_category_summary.csv")
except Exception as e:
    st.error("Could not load cleaned data files.")
    st.exception(e)
    st.stop()

st.subheader("📈 Monthly Sales (Sample)")
st.dataframe(monthly.head(10))

st.subheader("🏬 Category Summary (Food vs Beverage)")
st.dataframe(category.head(10))

st.success("Dashboard loaded successfully ✅")
