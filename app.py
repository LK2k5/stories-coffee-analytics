import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Stories Coffee Dashboard", layout="wide")

st.title("☕ Stories Coffee — Sales & Profitability Dashboard")
st.caption("Built from POS exports (2025 + Jan 2026). Numbers are in arbitrary units; focus on patterns.")

# --- Load data (default from outputs/)
OUT_DIR = Path("outputs")

@st.cache_data
def load_default():
    monthly = pd.read_csv(OUT_DIR / "clean_monthly_sales_file1.csv")
    cat = pd.read_csv(OUT_DIR / "clean_category_summary.csv")
    prod = None
    prod_path = OUT_DIR / "clean_items_file2.csv"
    if prod_path.exists():
        prod = pd.read_csv(prod_path)
    return monthly, cat, prod

# --- Sidebar: user can upload cleaned files (future-proof)
st.sidebar.header("Data Input")
use_upload = st.sidebar.checkbox("Upload cleaned CSVs instead of using outputs/")

monthly, cat, prod = load_default()

if use_upload:
    up_monthly = st.sidebar.file_uploader("Upload clean_monthly_sales_file1.csv", type=["csv"])
    up_cat = st.sidebar.file_uploader("Upload clean_category_summary.csv", type=["csv"])
    up_prod = st.sidebar.file_uploader("Upload clean_items_file2.csv (optional)", type=["csv"])

    if up_monthly is not None:
        monthly = pd.read_csv(up_monthly)
    if up_cat is not None:
        cat = pd.read_csv(up_cat)
    if up_prod is not None:
        prod = pd.read_csv(up_prod)

# --- Quick guards
required_month_cols = {"year","branch","total_calc"}
if not required_month_cols.issubset(set(monthly.columns)):
    st.error(f"Monthly file missing columns: {required_month_cols - set(monthly.columns)}")
    st.stop()

if not {"branch","Category","Revenue","Total Profit"}.issubset(set(cat.columns)):
    st.error("Category summary file missing expected columns (branch, Category, Revenue, Total Profit).")
    st.stop()

# --- Filters
st.sidebar.header("Filters")
years = sorted([y for y in monthly["year"].dropna().unique()])
year_choice = st.sidebar.selectbox("Year", years, index=0)
show_top_n = st.sidebar.slider("Top N branches", 5, 25, 10)

m = monthly[monthly["year"] == year_choice].copy()

# --- Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Top {show_top_n} Branches by Total Sales ({int(year_choice)})")
    top = m.sort_values("total_calc", ascending=False).head(show_top_n)[["branch","total_calc"]]
    st.bar_chart(top.set_index("branch"))

with col2:
    st.subheader(f"Seasonality ({int(year_choice)})")
    months = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    existing_months = [c for c in months if c in m.columns]
    if len(existing_months) >= 3:
        season = m[existing_months].sum().rename("total")
        st.line_chart(season)
        st.caption("Note: spikes can reflect seasonality and/or reporting coverage differences.")
    else:
        st.info("Monthly columns not found (jan..dec).")

st.divider()

# --- Profitability
st.subheader("Profitability by Branch (Food + Beverages)")
branch_margin = cat.groupby("branch")[["Total Profit","Revenue"]].sum()
branch_margin["margin"] = branch_margin["Total Profit"] / branch_margin["Revenue"]
branch_margin = branch_margin.sort_values("margin", ascending=False)

col3, col4 = st.columns(2)
with col3:
    st.write("Top 15 branches by profit margin")
    st.bar_chart(branch_margin.head(15)["margin"])

with col4:
    st.write("Bottom 15 branches by profit margin")
    st.bar_chart(branch_margin.tail(15)["margin"])

st.divider()

# --- Category mix
st.subheader("Beverage vs Food Revenue Share by Branch")
mix = cat.pivot_table(index="branch", columns="Category", values="Revenue", aggfunc="sum").fillna(0)
mix["Total"] = mix.sum(axis=1)
mix["BEV_share"] = mix.get("BEVERAGES", 0) / mix["Total"]
mix["FOOD_share"] = mix.get("FOOD", 0) / mix["Total"]
mix = mix.sort_values("BEV_share", ascending=False)

st.dataframe(
    mix[["BEV_share","FOOD_share"]].head(20),
    use_container_width=True
)

st.divider()

# --- Product-level quick wins (if file2 exists)
st.subheader("Menu Engineering (Product Profitability) — Quick Wins")
if prod is None:
    st.info("Upload or generate clean_items_file2.csv to see product-level insights.")
else:
    # Expect common columns; adapt if needed
    # Try to infer column names
    col_desc = None
    for candidate in ["Product Desc", "product_desc", "Description", "desc"]:
        if candidate in prod.columns:
            col_desc = candidate
            break

    if col_desc is None:
        st.warning("Could not find product description column in clean_items_file2.csv.")
    else:
        # Ensure needed numeric columns exist
        for c in ["Qty","Total Cost","Total Profit","Revenue"]:
            if c not in prod.columns:
                st.warning(f"Missing column '{c}' in product file. Export from cleaning with these fields if possible.")
                break
        else:
            prod2 = prod.copy()
            prod2["margin"] = prod2["Total Profit"] / prod2["Revenue"]
            prod2["profit_per_unit"] = prod2["Total Profit"] / prod2["Qty"]

            top_profit = prod2.sort_values("Total Profit", ascending=False).head(15)[[col_desc,"Qty","Revenue","Total Profit","margin","profit_per_unit"]]
            st.write("Top 15 products by total profit")
            st.dataframe(top_profit, use_container_width=True)

            st.write("Top 15 products by profit per unit (avoid tiny-Qty items by filtering)")
            min_qty = st.slider("Min Qty filter", 0, 500, 50)
            top_ppu = prod2[prod2["Qty"] >= min_qty].sort_values("profit_per_unit", ascending=False).head(15)[[col_desc,"Qty","Revenue","Total Profit","margin","profit_per_unit"]]
            st.dataframe(top_ppu, use_container_width=True)

st.caption("Tip: This dashboard is designed to work with future monthly exports by uploading updated cleaned CSVs.")
