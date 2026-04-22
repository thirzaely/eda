import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Customer Dashboard", layout="wide")
st.title("📊 Customer Analysis Dashboard")

# LOAD DATA
@st.cache_data
def load_data():
    if not os.path.exists("main_table.csv"):
        return None
    return pd.read_csv("main_table.csv")

df = load_data()

if df is None:
    st.error("File tidak ditemukan")
    st.stop()

# ======================
# FILTER (INTERAKTIF)
# ======================
st.sidebar.header("Filter")

segment_filter = st.sidebar.multiselect(
    "Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

df_filtered = df[df["Segment"].isin(segment_filter)]

# ======================
# MENU (SIMPLIFIED)
# ======================
menu = st.sidebar.radio("Menu", ["RFM", "Geospatial"])

# ======================
# RFM
# ======================
if menu == "RFM":
    st.header("👥 RFM Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Jumlah Customer per Segment")
        st.bar_chart(df_filtered["Segment"].value_counts())

    with col2:
        st.subheader("Revenue per Segment")
        st.bar_chart(df_filtered.groupby("Segment")["Monetary"].sum())

    st.markdown("""
    **Insight:**
    - Segment tertentu mendominasi jumlah customer
    - Revenue tidak tersebar merata antar segment
    """)

# ======================
# GEOSPATIAL
# ======================
elif menu == "Geospatial":
    st.header("🌍 Geospatial Analysis")

    geo = df_filtered.groupby("customer_city").agg(
        total_customer=("customer_id", "count"),
        total_revenue=("Monetary", "sum")
    ).reset_index()

    top_city = geo.sort_values("total_customer", ascending=False).head(10)

    st.subheader("Top Kota berdasarkan Customer")

    st.bar_chart(top_city.set_index("customer_city")["total_customer"])

    st.markdown("""
    **Insight:**
    - Kota dengan customer terbanyak tidak selalu menghasilkan revenue tertinggi
    """)
