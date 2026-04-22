import streamlit as st

st.write("🔥 APP STARTED - DEBUG 1")

import pandas as pd
import matplotlib.pyplot as plt
import os

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Customer Analysis Dashboard",
    layout="wide"
)

st.title("📊 Customer Analysis Dashboard")

st.write("APP STARTED")

# ======================
# CEK FILE
# ======================
if not os.path.exists("main_table.csv"):
    st.error("File main_table.csv tidak ditemukan di repository")
    st.stop()

# ======================
# LOAD DATA (SAFE)
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

    st.subheader("Distribusi Revenue")

    fig, ax = plt.subplots()
    ax.hist(df["Monetary"].dropna(), bins=20)
    ax.set_title("Distribusi Monetary")
    st.pyplot(fig)

    # ===== INSIGHT DATA-DRIVEN =====
    median_val = df["Monetary"].median()
    max_val = df["Monetary"].max()

    st.markdown(f"""
    **Insight:**
    - Median transaksi pelanggan adalah **{median_val:,.0f}**
    - Terdapat outlier hingga **{max_val:,.0f}**
    - Distribusi menunjukkan kecenderungan skew ke kanan
    """)

# ======================
# RFM ANALYSIS
# ======================
elif menu == "RFM Analysis":
    st.header("👥 RFM Analysis")

    st.subheader("Distribusi Segment")

    fig, ax = plt.subplots()
    df["Segment"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Revenue per Segment")

    seg_revenue = df.groupby("Segment")["Monetary"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots()
    seg_revenue.plot(kind="bar", ax=ax)
    st.pyplot(fig)

    # ===== INSIGHT DATA-DRIVEN =====
    top_segment = seg_revenue.idxmax()
    top_value = seg_revenue.max()

    st.markdown(f"""
    **Insight:**
    - Segment dengan kontribusi terbesar adalah **{top_segment}**
    - Kontribusi tertinggi mencapai **{top_value:,.0f}**
    - Terdapat ketimpangan kontribusi antar segment
    """)

# ======================
# GEOSPATIAL (city analysis)
# ======================
elif menu == "Geospatial":
    st.header("🌍 City Analysis")

    geo = df.groupby("customer_city").agg({
        "customer_id": "count",
        "Monetary": "sum"
    }).reset_index()

    geo.columns = ["city", "total_customers", "total_revenue"]

    top_city = geo.sort_values("total_customers", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.bar(top_city["city"], top_city["total_customers"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ===== INSIGHT DATA-DRIVEN =====
    best_city = geo.sort_values("total_revenue", ascending=False).iloc[0]

    st.markdown(f"""
    **Insight:**
    - Kota dengan revenue tertinggi adalah **{best_city['city']}**
    - Total revenue mencapai **{best_city['total_revenue']:,.0f}**
    - Tidak semua kota dengan banyak customer menghasilkan revenue tinggi
    """)

# ======================
# CUSTOMER BEHAVIOR
# ======================
elif menu == "Customer Behavior":
    st.header("📈 Customer Behavior")

    fig, ax = plt.subplots()
    ax.scatter(df["Frequency"], df["Monetary"])
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Monetary")
    st.pyplot(fig)

    # ===== INSIGHT DATA-DRIVEN =====
    avg_freq = df["Frequency"].mean()
    avg_monetary = df["Monetary"].mean()

    st.markdown(f"""
    **Insight:**
    - Rata-rata frekuensi transaksi: **{avg_freq:.2f}**
    - Rata-rata pengeluaran: **{avg_monetary:,.0f}**
    - Mayoritas pelanggan berada di area low-frequency segment
    """)
