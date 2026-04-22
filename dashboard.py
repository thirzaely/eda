import streamlit as st
import pandas as pd
import os

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Customer Analysis Dashboard",
    layout="wide"
)

st.title("📊 Customer Analysis Dashboard")

st.write("🔥 APP STARTED")

# ======================
# CEK FILE
# ======================
if not os.path.exists("main_table.csv"):
    st.error("File main_table.csv tidak ditemukan di repository")
    st.stop()

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("main_table.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.write("Kolom dataset:", df.columns.tolist())

# ======================
# VALIDASI KOLOM
# ======================
required_cols = ["customer_id", "Monetary", "Frequency", "Segment", "customer_city"]

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Kolom hilang: {missing}")
    st.stop()

# ======================
# SIDEBAR MENU
# ======================
st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Overview", "RFM Analysis", "Geospatial", "Customer Behavior"]
)

# ======================
# OVERVIEW
# ======================
if menu == "Overview":
    st.header("📊 Overview")

    col1, col2 = st.columns(2)

    total_customer = df["customer_id"].nunique()
    total_revenue = df["Monetary"].sum()

    col1.metric("Total Customer", total_customer)
    col2.metric("Total Revenue", f"{total_revenue:,.0f}")

    st.subheader("Distribusi Revenue (Simplified)")

    st.bar_chart(df["Monetary"])

    median_val = df["Monetary"].median()
    max_val = df["Monetary"].max()

    st.markdown(f"""
    **Insight:**
    - Median transaksi pelanggan: **{median_val:,.0f}**
    - Nilai maksimum: **{max_val:,.0f}**
    - Distribusi cenderung tidak merata
    """)

# ======================
# RFM ANALYSIS
# ======================
elif menu == "RFM Analysis":
    st.header("👥 RFM Analysis")

    st.subheader("Distribusi Segment")

    segment_count = df["Segment"].value_counts()
    st.bar_chart(segment_count)

    st.subheader("Revenue per Segment")

    seg_revenue = df.groupby("Segment")["Monetary"].sum().sort_values(ascending=False)
    st.bar_chart(seg_revenue)

    top_segment = seg_revenue.idxmax()
    top_value = seg_revenue.max()

    st.markdown(f"""
    **Insight:**
    - Segment terbesar: **{top_segment}**
    - Kontribusi revenue: **{top_value:,.0f}**
    - Distribusi tidak merata antar segment
    """)

# ======================
# GEOSPATIAL
# ======================
elif menu == "Geospatial":
    st.header("🌍 City Analysis")

    geo = df.groupby("customer_city").agg({
        "customer_id": "count",
        "Monetary": "sum"
    }).reset_index()

    geo.columns = ["city", "total_customers", "total_revenue"]

    top_city = geo.sort_values("total_customers", ascending=False).head(10)

    st.bar_chart(top_city.set_index("city")["total_customers"])

    best_city = geo.sort_values("total_revenue", ascending=False).iloc[0]

    st.markdown(f"""
    **Insight:**
    - Kota tertinggi revenue: **{best_city['city']}**
    - Total revenue: **{best_city['total_revenue']:,.0f}**
    - Tidak semua kota dengan banyak customer menghasilkan revenue tinggi
    """)

# ======================
# CUSTOMER BEHAVIOR
# ======================
elif menu == "Customer Behavior":
    st.header("📈 Customer Behavior")

    st.subheader("Frequency vs Monetary")

    st.scatter_chart(df[["Frequency", "Monetary"]])

    avg_freq = df["Frequency"].mean()
    avg_monetary = df["Monetary"].mean()

    st.markdown(f"""
    **Insight:**
    - Rata-rata frequency: **{avg_freq:.2f}**
    - Rata-rata monetary: **{avg_monetary:,.0f}**
    - Mayoritas pelanggan berada di low-frequency segment
    """)
