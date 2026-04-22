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
# VALIDASI
# ======================
if df is None:
    st.error("File main_table.csv tidak ditemukan")
    st.stop()

required_cols = ["customer_id", "Monetary", "Frequency", "Segment", "customer_city"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Kolom kurang: {missing}")
    st.stop()

# ======================
# FILTER (INI KUNCI K4)
# ======================
st.sidebar.title("Filter Data")

segment_filter = st.sidebar.multiselect(
    "Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

city_filter = st.sidebar.multiselect(
    "Kota",
    options=df["customer_city"].unique(),
    default=df["customer_city"].unique()
)

min_money = float(df["Monetary"].min())
max_money = float(df["Monetary"].max())

money_filter = st.sidebar.slider(
    "Range Monetary",
    min_money,
    max_money,
    (min_money, max_money)
)

# ======================
# FILTERED DATA (WAJIB)
# ======================
df_filtered = df[
    (df["Segment"].isin(segment_filter)) &
    (df["customer_city"].isin(city_filter)) &
    (df["Monetary"] >= money_filter[0]) &
    (df["Monetary"] <= money_filter[1])
]

st.sidebar.markdown("---")
st.sidebar.write(f"Data terfilter: {df_filtered.shape[0]} baris")

# ======================
# MENU
# ======================
menu = st.sidebar.radio(
    "Menu",
    ["Overview", "RFM Analysis", "Geospatial", "Customer Behavior"]
)

# ======================
# OVERVIEW
# ======================
if menu == "Overview":
    st.header("📊 Overview")

    col1, col2 = st.columns(2)

    col1.metric("Total Customer", df_filtered["customer_id"].nunique())
    col2.metric("Total Revenue", f"{df_filtered['Monetary'].sum():,.0f}")

    st.subheader("Distribusi Monetary")

    st.bar_chart(df_filtered["Monetary"])

    st.markdown("""
    **Insight:**
    - Mayoritas transaksi bernilai rendah
    - Data sangat dipengaruhi oleh customer dengan transaksi kecil
    """)

# ======================
# RFM ANALYSIS
# ======================
elif menu == "RFM Analysis":
    st.header("👥 RFM Analysis")

    segment_count = df_filtered["Segment"].value_counts()
    segment_revenue = df_filtered.groupby("Segment")["Monetary"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Jumlah Customer per Segment")
        st.bar_chart(segment_count)

    with col2:
        st.subheader("Revenue per Segment")
        st.bar_chart(segment_revenue)

    st.markdown(f"""
    **Insight:**
    - Segment terbesar: **{segment_count.idxmax()}**
    - Revenue tertinggi: **{segment_revenue.idxmax()}**
    - Distribusi tidak merata antar segment
    """)

# ======================
# GEOSPATIAL (CITY ANALYSIS)
# ======================
elif menu == "Geospatial":
    st.header("🌍 Geospatial Analysis")

    geo = df_filtered.groupby("customer_city").agg(
        total_customers=("customer_id", "count"),
        total_revenue=("Monetary", "sum")
    ).reset_index()

    top_city = geo.sort_values("total_customers", ascending=False).head(10)

    st.subheader("Top City by Customer")

    st.bar_chart(top_city.set_index("customer_city")["total_customers"])

    best_city = geo.sort_values("total_revenue", ascending=False).iloc[0]

    st.markdown(f"""
    **Insight:**
    - Kota revenue tertinggi: **{best_city['customer_city']}**
    - Total revenue: **{best_city['total_revenue']:,.0f}**
    - Tidak semua kota dengan banyak customer menghasilkan revenue tinggi
    """)

# ======================
# CUSTOMER BEHAVIOR
# ======================
elif menu == "Customer Behavior":
    st.header("📈 Customer Behavior")

    st.subheader("Frequency vs Monetary")

    st.scatter_chart(df_filtered[["Frequency", "Monetary"]])

    st.markdown(f"""
    **Insight:**
    - Rata-rata frequency: **{df_filtered["Frequency"].mean():.2f}**
    - Rata-rata monetary: **{df_filtered["Monetary"].mean():,.0f}**
    - Mayoritas customer low engagement
    """)
