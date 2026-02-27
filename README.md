# Air Quality Analysis Dashboard 🌦️

## Struktur Folder
- `dashboard/`: Berisi `dashboard.py` dan `main_data.csv`.
- `data/`: Berisi dataset mentah (CSV).
- `notebook.ipynb`: File analisis data (Gathering hingga EDA).
- `requirements.txt`: Daftar library (Pandas, Matplotlib, Seaborn, Streamlit).
- `README.md`: Dokumentasi proyek.

## Cara Menjalankan (Lokal)
1. **Masuk ke Folder:**
    Buka folder submission lewat File Explorer. 
    Klik pada Address Bar di bagian atas folder (yang ada tulisan C:\Users\Documents\...) atau dibagian manapun km simpan, lalu select all kemudian hapus semua tulisannya, dan ketik cmd, lalu tekan Enter.
2. **Instal Library:**
   pip install -r requirements.txt
3. **Jalankan Dashboard:**
   python -m streamlit run dashboard/dashboard.py
4. **Voila! Sudah ke run di lokal**
    biasanya akan langsung ke direct ke http://localhost:8501/