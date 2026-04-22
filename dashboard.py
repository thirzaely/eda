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

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    if not os.path.exists("main_table.csv"):
        return None

    df = pd.read_csv("main_table.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ======================
# VALIDASI DATA
# ======================
if df is None:
    st.error("File main_table.csv tidak ditemukan di repository")
    st.stop()

required_cols = ["customer_id", "Monetary", "Frequency", "Segment", "customer_city"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Kolom tidak lengkap: {missing}")
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

    col1.metric("Total Customer", df["customer_id"].nunique())
    col2.metric("Total Revenue", f"{df['Monetary'].sum():,.0f}")

    st.subheader("Distribusi Revenue")

    st.bar_chart(df["Monetary"])

    st.markdown(f"""
    **Insight:**
    - Median transaksi: **{df["Monetary"].median():,.0f}**
    - Maksimum transaksi: **{df["Monetary"].max():,.0f}**
    - Distribusi menunjukkan ketimpangan nilai transaksi
    """)

# ======================
# RFM ANALYSIS
# ======================
elif menu == "RFM Analysis":
    st.header("👥 RFM Analysis")

    segment_count = df["Segment"].value_counts()
    seg_revenue = df.groupby("Segment")["Monetary"].sum().sort_values(ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Segment")
        st.bar_chart(segment_count)

    with col2:
        st.subheader("Revenue per Segment")
        st.bar_chart(seg_revenue)

    st.markdown(f"""
    **Insight:**
    - Segment dominan: **{seg_revenue.idxmax()}**
    - Kontribusi terbesar: **{seg_revenue.max():,.0f}**
    - Distribusi revenue tidak merata antar segment
    """)

# ======================
# GEOSPATIAL
# ======================
elif menu == "Geospatial":
    st.header("🌍 City Analysis")

    geo = df.groupby("customer_city").agg(
        total_customers=("customer_id", "count"),
        total_revenue=("Monetary", "sum")
    ).reset_index()

    top_city = geo.sort_values("total_customers", ascending=False).head(10)

    st.subheader("Top City by Customer")

    st.bar_chart(top_city.set_index("customer_city")["total_customers"])

    best_city = geo.sort_values("total_revenue", ascending=False).iloc[0]

    st.markdown(f"""
    **Insight:**
    - Kota dengan revenue tertinggi: **{best_city['customer_city']}**
    - Total revenue: **{best_city['total_revenue']:,.0f}**
    - Jumlah customer tidak selalu sejalan dengan revenue
    """)

# ======================
# CUSTOMER BEHAVIOR
# ======================
elif menu == "Customer Behavior":
    st.header("📈 Customer Behavior")

    st.subheader("Frequency vs Monetary")

    st.scatter_chart(df[["Frequency", "Monetary"]])

    st.markdown(f"""
    **Insight:**
    - Rata-rata frequency: **{df["Frequency"].mean():.2f}**
    - Rata-rata monetary: **{df["Monetary"].mean():,.0f}**
    - Mayoritas customer berada pada low engagement segment
    """)
