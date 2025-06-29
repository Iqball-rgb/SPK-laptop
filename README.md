# Sistem Pendukung Keputusan (SPK) Pemilihan Laptop

<p align="center">
  <img src="https://github.com/Iqball-rgb/SPK-laptop/blob/d84dc885b0ce1a2495d28eb70a81a30defb421bd/logo2.png" alt="Logo SPK Laptop" width="150">
</p>
<p align="center">
  Aplikasi web interaktif untuk membantu pengguna memilih laptop terbaik berdasarkan kriteria dan preferensi pribadi menggunakan metode Weighted Product (WP) dan Multi-Attribute Utility Theory (MAUT).
</p>

---

## 🚀 Deskripsi Proyek
Proyek ini adalah sebuah aplikasi berbasis web yang dibangun dengan Streamlit untuk mengimplementasikan Sistem Pendukung Keputusan (SPK). Tujuannya adalah untuk memberikan rekomendasi laptop yang paling sesuai bagi pengguna berdasarkan pembobotan kriteria yang dapat diatur, seperti harga, RAM, storage, performa prosesor (CPU), dan kartu grafis (GPU).

Aplikasi ini dirancang untuk menjadi alat bantu praktis bagi calon pembeli laptop yang bingung dalam menentukan pilihan di antara banyak alternatif yang tersedia di pasar.

## ✨ Fitur Utama
- **Login Berbasis Pengguna:** Sistem login sederhana menggunakan nama pengguna untuk memisahkan data dan preferensi setiap user.
- **Manajemen Data Laptop:** Pengguna dapat menambah, melihat, mengedit, dan menghapus data alternatif laptop.
- **Skoring Komponen Otomatis:** Sistem secara cerdas memberikan skor numerik untuk CPU dan GPU menggunakan pencocokan pola (Regex) untuk menangani berbagai format penulisan.
- **Pembobotan Kriteria Dinamis:** Pengguna dapat mengatur bobot (prioritas) untuk setiap kriteria (misalnya, lebih mementingkan harga murah atau performa GPU).
- **Upload Data dari Excel:** Memudahkan input data dalam jumlah banyak dengan mengunggah file `.xlsx`.
- **Perhitungan Dua Metode SPK:**
    1.  **Weighted Product (WP):** Menggunakan konversi ke Skala Likert untuk menormalisasi data sebelum perhitungan.
    2.  **Multi-Attribute Utility Theory (MAUT):** Menggunakan normalisasi Min-Max untuk mengubah nilai setiap kriteria ke dalam skala utilitas (0-1).
- **Visualisasi Hasil:** Hasil perankingan disajikan dalam bentuk tabel dan grafik batang interaktif untuk kemudahan analisis.
- **Detail Perhitungan Transparan:** Aplikasi menyediakan tab khusus untuk melihat detail proses perhitungan WP dan MAUT, dari data awal hingga skor akhir.

## ⚙️ Metode SPK yang Digunakan

### 1. Multi-Attribute Utility Theory (MAUT)
MAUT bekerja dengan mengubah setiap nilai kriteria menjadi nilai utilitas dalam rentang 0 hingga 1. Rumus normalisasi Min-Max yang digunakan adalah:

- **Untuk Kriteria Benefit (semakin besar semakin baik):**
  $$ U(x) = \frac{x - x_{min}}{x_{max} - x_{min}} $$
- **Untuk Kriteria Cost (semakin kecil semakin baik):**
  $$ U(x) = \frac{x_{max} - x}{x_{max} - x_{min}} $$

Skor akhir setiap alternatif adalah jumlah dari perkalian nilai utilitas dengan bobot kriteria.

### 2. Weighted Product (WP)
Metode WP melakukan perhitungan dengan perkalian, di mana setiap kriteria dipangkatkan dengan bobotnya. Dalam aplikasi ini, nilai asli setiap kriteria (harga, RAM, dll.) pertama-tama dikonversi ke **Skala Likert (1-5)** untuk menyeragamkan skala penilaian sebelum proses pemangkatan dilakukan.

## 🛠️ Teknologi yang Digunakan
- **Python:** Bahasa pemrograman utama.
- **Streamlit:** Framework untuk membangun aplikasi web.
- **Pandas:** Untuk manipulasi dan analisis data.
- **NumPy:** Untuk komputasi numerik.
- **Plotly:** Untuk membuat grafik interaktif.
- **SQLite:** Database engine untuk penyimpanan data.

## 💻 Cara Menjalankan Proyek Secara Lokal

1.  **Clone Repositori**
    ```bash
    git clone [https://github.com/username/nama-repo.git](https://github.com/username/nama-repo.git)
    cd nama-repo
    ```

2.  **Buat dan Aktifkan Virtual Environment** (direkomendasikan)
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependensi**
    Pastikan Anda memiliki file `requirements.txt` di dalam folder.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Streamlit**
    Ganti `nama_file.py` dengan nama file Python utama Anda.
    ```bash
    streamlit run nama_file.py
    ```

---

