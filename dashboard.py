import streamlit as st
import pandas as pd
import os

# CONFIG
st.set_page_config(page_title="Customer Dashboard", layout="wide")
st.title("📊 Customer Analysis Dashboard")

# LOAD DATA
@st.cache_data
def load_data():
    if not os.path.exists("main_table.csv"):
        return None
    df = pd.read_csv("main_table.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

if df is None:
    st.error("File main_table.csv tidak ditemukan")
    st.stop()

# VALIDASI
required_cols = ["customer_id", "Monetary", "Frequency", "Segment", "customer_city"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Kolom tidak lengkap: {missing}")
    st.stop()

# FILTER
st.sidebar.header("Filter Data")

segment_filter = st.sidebar.multiselect(
    "Pilih Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

df_filtered = df[df["Segment"].isin(segment_filter)]

st.sidebar.markdown(f"**Data terfilter:** {df_filtered.shape[0]} baris")

# MENU
menu = st.sidebar.radio("Menu", ["RFM Analysis", "Geospatial"])

# RFM ANALYSIS
if menu == "RFM Analysis":
    st.header("👥 RFM Analysis")

    segment_order = df_filtered["Segment"].value_counts().index

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Jumlah Customer per Segment")
        seg_count = df_filtered["Segment"].value_counts().reindex(segment_order)
        st.bar_chart(seg_count)

    with col2:
        st.subheader("Revenue per Segment")
        seg_rev = df_filtered.groupby("Segment")["Monetary"].sum().reindex(segment_order)
        st.bar_chart(seg_rev)

    st.subheader("Karakteristik Perilaku (Frequency vs Monetary)")
    st.scatter_chart(df_filtered[["Frequency", "Monetary"]])

    st.markdown("""
    **Insight:**
    - Distribusi customer tidak seimbang antar segment
    - Segment dengan jumlah customer besar tidak selalu memiliki kontribusi revenue terbesar
    - Mayoritas customer memiliki frequency rendah dan monetary rendah
    - Terdapat sebagian kecil customer dengan monetary tinggi (high value customer)
    """)

# GEOSPATIAL ANALYSIS
elif menu == "Geospatial":
    st.header("🌍 Geospatial Analysis")

    geo = df_filtered.groupby("customer_city").agg(
        total_customer=("customer_id", "count"),
        total_revenue=("Monetary", "sum")
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Kota berdasarkan Customer")
        top_city = geo.sort_values("total_customer", ascending=False).head(10)
        st.bar_chart(top_city.set_index("customer_city")["total_customer"])

    with col2:
        st.subheader("Top 10 Kota berdasarkan Revenue")
        top_rev = geo.sort_values("total_revenue", ascending=False).head(10)
        st.bar_chart(top_rev.set_index("customer_city")["total_revenue"])

    st.subheader("Hubungan Customer vs Revenue")
    st.scatter_chart(geo[["total_customer", "total_revenue"]])

    st.markdown("""
    **Insight:**
    - Kota dengan jumlah customer tinggi tidak selalu menghasilkan revenue tinggi
    - Terdapat ketimpangan kontribusi antar wilayah
    - Beberapa kota memiliki potensi revenue tinggi meskipun jumlah customer tidak dominan
    """)
