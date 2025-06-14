# 💻 SPK Pemilihan Laptop Terbaik

Aplikasi Web berbasis Python & Streamlit untuk membantu memilih laptop terbaik berdasarkan kriteria pengguna.  
Metode yang digunakan:

- 🧮 **Weighted Product (WP)**
- 📈 **Multi Attribute Utility Theory (MAUT)**

## 📦 Fitur Aplikasi
- Login pengguna
- Tambah/edit/hapus data laptop
- Input bobot kriteria
- Upload data dari file Excel (multi-sheet, nama kolom fleksibel)
- Visualisasi hasil ranking
- Cegah duplikasi otomatis
- Hapus seluruh data pengguna

## 📁 Struktur File
- `web.py` : file utama aplikasi Streamlit
- `requirements.txt` : dependensi yang dibutuhkan
- `README.md` : dokumentasi proyek

## 🚀 Cara Menjalankan di Lokal
```bash
pip install -r requirements.txt
streamlit run web.py
