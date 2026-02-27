import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from datetime import datetime

# Set page title & layout
st.set_page_config(page_title="Air Quality Analysis Dashboard", layout="wide")

# --- LOAD & MERGE DATA (Sesuai Logika Notebook) ---
@st.cache_data
def load_data():
    # Menggabungkan semua CSV stasiun seperti di Notebook
    data_path = "data/" 
    try:
        all_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
        df_list = []
        for file in all_files:
            df_list.append(pd.read_csv(os.path.join(data_path, file)))
        
        df = pd.concat(df_list, ignore_index=True)
        
        # Konversi datetime (Penting untuk Tren Bulanan)
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        
        # Cleaning simpel agar dashboard stabil
        df = df.ffill().bfill() 
        return df
    except Exception as e:
        # Fallback jika folder data tidak ketemu, coba baca main_data.csv langsung
        return pd.read_csv("dashboard/main_data.csv", parse_dates=['datetime'])

# Memuat data
all_df = load_data()

# --- SIDEBAR ---
st.sidebar.header("Filter Eksplorasi")

# 1. Filter Stasiun
station_list = sorted(all_df['station'].unique())
selected_stations = st.sidebar.multiselect(
    "Pilih Stasiun Pemantau:",
    options=station_list,
    default=station_list
)

# 2. Filter Rentang Waktu
min_date = all_df['datetime'].min().date()
max_date = all_df['datetime'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter Data Berdasarkan Sidebar
main_df = all_df[
    (all_df['station'].isin(selected_stations)) & 
    (all_df['datetime'].dt.date >= start_date) & 
    (all_df['datetime'].dt.date <= end_date)
]

# --- MAIN PAGE ---
st.title("🌦️ Air Quality Analysis Dashboard")
st.markdown(f"Menampilkan data dari **{len(selected_stations)} stasiun**")

# Row 1: Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rata-rata PM2.5", f"{main_df['PM2.5'].mean():.2f} µg/m³")
with col2:
    st.metric("Rata-rata Ozon (O3)", f"{main_df['O3'].mean():.2f} µg/m³")
with col3:
    st.metric("Rata-rata Suhu", f"{main_df['TEMP'].mean():.2f} °C")

st.divider()

# Row 2: Pertanyaan 1 (Tren Bulanan)
st.subheader("1. Tren Bulanan Konsentrasi PM2.5")
fig_monthly, ax_monthly = plt.subplots(figsize=(12, 5))
monthly_trend = main_df.set_index('datetime').resample('M')['PM2.5'].mean().reset_index()
sns.lineplot(data=monthly_trend, x='datetime', y='PM2.5', marker='o', color='#2E86C1', ax=ax_monthly)
ax_monthly.set_ylabel("Konsentrasi PM2.5")
st.pyplot(fig_monthly)

# Row 3: Pertanyaan 2 (Korelasi TEMP vs O3)
st.subheader("2. Hubungan Suhu (TEMP) terhadap Ozon (O3)")
fig_corr, ax_corr = plt.subplots(figsize=(10, 5))
sample_size = min(5000, len(main_df))
sns.regplot(data=main_df.sample(sample_size), x='TEMP', y='O3', 
            scatter_kws={'alpha':0.3, 'color':'#27AE60'}, line_kws={'color':'red'}, ax=ax_corr)
ax_corr.set_xlabel("Suhu (°C)")
ax_corr.set_ylabel("Ozon (O3)")
st.pyplot(fig_corr)

st.divider()

# --- CONCLUSION SECTION (WAJIB ADA) ---
st.subheader("📌 Conclusion")
with st.container():
    st.markdown(f"""
    **Pertanyaan 1: Tren rata-rata bulanan PM2.5 (2013-2017)**
    - Berdasarkan visualisasi, konsentrasi **PM2.5** menunjukkan pola musiman yang sangat jelas. Polusi cenderung memuncak pada **musim dingin (Desember-Februari)** dan menurun secara signifikan saat musim panas. Hal ini dipengaruhi oleh peningkatan emisi pemanas ruangan dan kondisi atmosfer di Beijing.

    **Pertanyaan 2: Korelasi Suhu (TEMP) dengan Ozon (O3)**
    - Terdapat **korelasi positif yang signifikan (0.59)** antara suhu udara dan konsentrasi Ozon. Garis regresi menunjukkan bahwa setiap kenaikan suhu akan diikuti oleh kenaikan kadar Ozon. Hal ini membuktikan bahwa suhu tinggi adalah katalisator utama reaksi kimia polutan di atmosfer.
    """)

st.caption(f"Copyright (c) Chalida Abdat {datetime.now().year}")