import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Customer Analysis Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("main_table.csv")
    return df

df = load_data()

st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Overview", "RFM Analysis", "Geospatial", "Customer Behavior"]
)

if menu == "Overview":
    st.title("📊 Overview")

    col1, col2 = st.columns(2)

    col1.metric("Total Customer", df["customer_id"].nunique())
    col2.metric("Total Revenue", f"{df['Monetary'].sum():,.0f}")

    st.subheader("Distribusi Revenue Customer")

    fig, ax = plt.subplots()
    ax.hist(df["Monetary"])
    ax.set_title("Distribusi Monetary")
    st.pyplot(fig)

    st.markdown("""
    **Insight:**
    - Sebagian besar pelanggan memiliki nilai transaksi rendah.
    - Sebagian kecil pelanggan menyumbang sebagian besar revenue.
    """)

elif menu == "RFM Analysis":
    st.title("👥 RFM Analysis")

    st.subheader("Distribusi Segmen Pelanggan")

    fig, ax = plt.subplots()
    df["Segment"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Kontribusi Revenue per Segmen")

    fig, ax = plt.subplots()
    df.groupby("Segment")["Monetary"].sum().sort_values(ascending=False).plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Rata-rata Pengeluaran per Segmen")

    fig, ax = plt.subplots()
    df.groupby("Segment")["Monetary"].mean().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.markdown("""
    **Insight:**
    - Segmen Champions memberikan kontribusi terbesar terhadap revenue.
    - Revenue tidak tersebar merata di semua pelanggan.
    """)

elif menu == "Geospatial":
    st.title("🌍 Geospatial Analysis")

    # AGREGASI DARI MAIN TABLE (WAJIB)
    geo = df.groupby("customer_city").agg({
        "customer_id": "count",
        "Monetary": "sum"
    }).reset_index()

    geo.columns = ["city", "total_customers", "total_revenue"]

    st.subheader("Top Kota Berdasarkan Jumlah Customer")

    top_city = geo.sort_values("total_customers", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.bar(top_city["city"], top_city["total_customers"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Top Kota Berdasarkan Revenue")

    top_revenue = geo.sort_values("total_revenue", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.bar(top_revenue["city"], top_revenue["total_revenue"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Transaksi vs Revenue")

    fig, ax = plt.subplots()
    ax.scatter(geo["total_customers"], geo["total_revenue"])
    ax.set_xlabel("Jumlah Customer")
    ax.set_ylabel("Total Revenue")
    st.pyplot(fig)

    st.markdown("""
    **Insight:**
    - Tidak semua kota dengan customer banyak menghasilkan revenue tinggi.
    - Terdapat perbedaan karakteristik pasar antar wilayah.
    """)

elif menu == "Customer Behavior":
    st.title("📈 Customer Behavior")

    st.subheader("Frequency vs Monetary")

    fig, ax = plt.subplots()
    ax.scatter(df["Frequency"], df["Monetary"])
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Monetary")
    st.pyplot(fig)

    st.subheader("Distribusi Tipe Pelanggan")

    if "Customer_Type" in df.columns:
        fig, ax = plt.subplots()
        df["Customer_Type"].value_counts().head(10).plot(kind="bar", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.markdown("""
    **Insight:**
    - Mayoritas pelanggan hanya melakukan satu transaksi.
    - Pelanggan bernilai tinggi tidak selalu memiliki frekuensi tinggi.
    """)

