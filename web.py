import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import os
from io import BytesIO

# ---------- CUSTOM CSS ----------
st.markdown(
    """
<style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #0073e6;
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        border: none;
        font-weight: 500;
    }
    .stTextInput>div>div>input {
        border-radius: 6px;
    }
    .stSelectbox>div>div>div {
        border-radius: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- SESSION INIT ----------
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ---------- LANDING PAGE ----------
if st.session_state.page == "landing":
    st.title("📊 SPK Pemilihan Laptop Terbaik")
    st.image("https://cdn-icons-png.flaticon.com/512/8090/8090406.png", width=100)
    st.markdown(
        """
    Selamat datang di **Sistem Pendukung Keputusan** untuk membantu memilih laptop terbaik
    berdasarkan kriteria yang kamu tentukan.

    Aplikasi ini menggunakan metode:
    - 🔹 **Weighted Product (WP)**
    - 🔹 **Multi-Attribute Utility Theory (MAUT)**

    Kamu dapat:
    - Menambahkan data laptop
    - Mengatur bobot kriteria
    - Mengunggah data dari Excel
    - Melihat hasil perankingan dan grafik interaktif

    👉 Tekan tombol **Mulai Aplikasi** untuk login dan menggunakan fitur lengkap.
    """
    )
    if st.button("Mulai Aplikasi"):
        st.session_state.page = "login"
        st.rerun()
    st.stop()

# ---------- LOGIN ----------
if st.session_state.page == "login" and not st.session_state.username:
    st.title("🔐 Login Pengguna")
    username_input = st.text_input("Masukkan nama pengguna:")
    if st.button("Login") and username_input:
        st.session_state.username = username_input
        st.session_state.page = "app"
        st.rerun()
    st.stop()

# ---------- LOGOUT ----------
if st.sidebar.button("🚪 Keluar"):
    st.session_state.username = None
    st.session_state.page = "landing"
    st.rerun()

# ---------- DATABASE SETUP ----------
DB_PATH = "laptop_spk.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

c.execute("PRAGMA table_info(laptops)")
cols = [col[1] for col in c.fetchall()]
if "username" not in cols and len(cols) > 0:
    conn.close()
    os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS laptops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    nama TEXT,
    harga INTEGER,
    ram INTEGER,
    storage INTEGER,
    prosesor TEXT,
    prosesor_skor INTEGER,
    gpu TEXT,
    gpu_skor INTEGER,
    layar REAL,
    rating REAL
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS bobot_kriteria (
    kriteria TEXT PRIMARY KEY,
    bobot REAL,
    tipe TEXT
)"""
)
conn.commit()

# ---------- FUNGSI & SKOR ----------
prosesor_scores = {
    "i3": 4,
    "i5": 6,
    "i7": 8,
    "i9": 10,
    "ryzen 3": 4,
    "ryzen 5": 6,
    "ryzen 7": 8,
    "ryzen 9": 10,
}
gpu_scores = {
    "intel uhd": 3,
    "iris xe": 4,
    "amd radeon": 5,
    "mx": 6,
    "gtx": 7,
    "rtx 2050": 8,
    "rtx 3050": 9,
    "rtx 3060": 10,
}


def get_skor(nama, skor_dict):
    nama = nama.lower()
    for key in skor_dict:
        if key in nama:
            return skor_dict[key]
    return 5


def insert_laptop(u, nama, harga, ram, storage, prosesor, gpu, layar, rating):
    ps = get_skor(prosesor, prosesor_scores)
    gs = get_skor(gpu, gpu_scores)
    c.execute(
        """INSERT INTO laptops (username, nama, harga, ram, storage, prosesor, prosesor_skor, gpu, gpu_skor, layar, rating)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            u,
            nama,
            int(harga),
            int(ram),
            int(storage),
            prosesor,
            ps,
            gpu,
            gs,
            float(layar),
            float(rating),
        ),
    )
    conn.commit()


def insert_if_not_exists(u, nama, harga, ram, storage, prosesor, gpu, layar, rating):
    c.execute(
        "SELECT COUNT(*) FROM laptops WHERE username=? AND nama=? AND prosesor=? AND ram=?",
        (u, nama, prosesor, ram),
    )
    if c.fetchone()[0] == 0:
        insert_laptop(u, nama, harga, ram, storage, prosesor, gpu, layar, rating)


def get_user_laptops():
    return pd.read_sql(
        "SELECT * FROM laptops WHERE username=?",
        conn,
        params=(st.session_state.username,),
    )


def delete_laptop(id):
    c.execute(
        "DELETE FROM laptops WHERE id=? AND username=?", (id, st.session_state.username)
    )
    conn.commit()


def update_laptop(id, nama, harga, ram, storage, prosesor, gpu, layar, rating):
    ps = get_skor(prosesor, prosesor_scores)
    gs = get_skor(gpu, gpu_scores)
    c.execute(
        """UPDATE laptops SET nama=?, harga=?, ram=?, storage=?, prosesor=?, prosesor_skor=?,
                 gpu=?, gpu_skor=?, layar=?, rating=? WHERE id=? AND username=?""",
        (
            nama,
            int(harga),
            int(ram),
            int(storage),
            prosesor,
            ps,
            gpu,
            gs,
            float(layar),
            float(rating),
            id,
            st.session_state.username,
        ),
    )
    conn.commit()


def update_bobot(b):
    c.execute("DELETE FROM bobot_kriteria")
    for k in b:
        tipe = "cost" if k == "harga" else "benefit"
        c.execute("INSERT INTO bobot_kriteria VALUES (?, ?, ?)", (k, b[k], tipe))
    conn.commit()


def get_bobot():
    df = pd.read_sql("SELECT * FROM bobot_kriteria", conn, index_col="kriteria")
    return df["bobot"].to_dict(), df["tipe"].to_dict()


def convert_df_to_excel(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()


# ---------- APP MAIN ----------
if st.session_state.page == "app":
    menu = st.sidebar.radio(
        "📌 Menu",
        [
            "➕ Tambah Data",
            "📄 Lihat Data",
            "⚖️ Input Bobot",
            "📂 Upload Excel",
            "📊 Rekomendasi",
        ],
    )
    st.header("📋 SPK Laptop — Menu " + menu.split()[1])

    if "Tambah" in menu:
        with st.form("form"):
            nama = st.text_input("Nama Laptop")
            harga = st.text_input("Harga")
            ram = st.text_input("RAM")
            storage = st.text_input("Storage")
            prosesor = st.text_input("Prosesor")
            gpu = st.text_input("GPU")
            layar = st.text_input("Layar")
            rating = st.text_input("Rating")
            if st.form_submit_button("Simpan"):
                insert_laptop(
                    st.session_state.username,
                    nama,
                    harga,
                    ram,
                    storage,
                    prosesor,
                    gpu,
                    layar,
                    rating,
                )
                st.success("Data disimpan.")

    elif "Lihat" in menu:
        df = get_user_laptops()
        st.dataframe(df)
        with st.expander("✏️ Edit Data"):
            if not df.empty:
                sid = st.selectbox("Pilih ID", df["id"])
                row = df[df["id"] == sid].iloc[0]
                with st.form("edit"):
                    n, h, r, s, p, g, l, rt = [
                        st.text_input("Nama", row["nama"]),
                        st.text_input("Harga", row["harga"]),
                        st.text_input("RAM", row["ram"]),
                        st.text_input("Storage", row["storage"]),
                        st.text_input("Prosesor", row["prosesor"]),
                        st.text_input("GPU", row["gpu"]),
                        st.text_input("Layar", row["layar"]),
                        st.text_input("Rating", row["rating"]),
                    ]
                    if st.form_submit_button("Update"):
                        update_laptop(sid, n, h, r, s, p, g, l, rt)
                        st.success("Berhasil diupdate.")
                        st.rerun()
        with st.expander("🗑️ Hapus Data"):
            did = st.number_input("ID", min_value=1)
            if st.button("Hapus"):
                delete_laptop(did)
                st.rerun()

    elif "Bobot" in menu:
        st.write("Masukkan bobot tiap kriteria (total 100%)")
        col = st.columns(7)
        bobot = dict(
            harga=col[0].number_input("Harga", 0, 100, 25),
            ram=col[1].number_input("RAM", 0, 100, 15),
            storage=col[2].number_input("Storage", 0, 100, 10),
            prosesor_skor=col[3].number_input("Prosesor", 0, 100, 20),
            gpu_skor=col[4].number_input("GPU", 0, 100, 20),
            layar=col[5].number_input("Layar", 0, 100, 5),
            rating=col[6].number_input("Rating", 0, 100, 5),
        )
        if sum(bobot.values()) == 100:
            if st.button("Simpan Bobot"):
                update_bobot({k: v / 100 for k, v in bobot.items()})
                st.success("Bobot disimpan.")
        else:
            st.error("Total bobot harus 100%")

    elif "Upload" in menu:
        import re

        keyword_map = {
            "Nama Laptop": [r"nama.*laptop", r"judul"],
            "Harga": [r"harga", r"price"],
            "RAM": [r"ram"],
            "Storage": [r"storage", r"ssd", r"hard.?disk"],
            "Prosesor": [r"prosesor", r"cpu"],
            "GPU": [r"gpu", r"vga", r"graphic"],
            "Layar": [r"layar", r"screen", r"display"],
            "Rating": [r"rating", r"review"],
        }

        def normalize_headers(df):
            renamed = {}
            for std_col, patterns in keyword_map.items():
                for col in df.columns:
                    for pat in patterns:
                        if re.search(pat, col.lower()):
                            renamed[col] = std_col
            return df.rename(columns=renamed)

        file = st.file_uploader("Upload file Excel", type=["xlsx"])
        if file:
            try:
                df = pd.read_excel(file)
                df = normalize_headers(df)
                inserted = 0
                for _, row in df.iterrows():
                    c.execute(
                        "SELECT COUNT(*) FROM laptops WHERE username=? AND nama=? AND prosesor=? AND ram=?",
                        (
                            st.session_state.username,
                            row["Nama Laptop"],
                            row["Prosesor"],
                            row["RAM"],
                        ),
                    )
                    if c.fetchone()[0] == 0:
                        insert_laptop(
                            st.session_state.username,
                            row["Nama Laptop"],
                            row["Harga"],
                            row["RAM"],
                            row["Storage"],
                            row["Prosesor"],
                            row["GPU"],
                            row["Layar"],
                            row["Rating"],
                        )
                        inserted += 1
                st.success(f"Berhasil menambahkan {inserted} data baru dari Excel.")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")

        st.divider()
        st.markdown("### 🧹 Hapus Semua Data Saya")
        if st.button("Hapus Semua Data Saya"):
            c.execute(
                "DELETE FROM laptops WHERE username=?", (st.session_state.username,)
            )
            conn.commit()
            st.success("Seluruh data Anda berhasil dihapus.")

    elif "Rekomendasi" in menu:
        try:
            df = get_user_laptops()
            bobot, tipe = get_bobot()
            norm = df.copy()
            for k in bobot:
                x = pd.to_numeric(norm[k], errors="coerce")
                norm[f"n_{k}"] = (x.min() / x) if tipe[k] == "cost" else (x / x.max())
            norm.dropna(inplace=True)
            norm["WP"] = np.prod([norm[f"n_{k}"] ** bobot[k] for k in bobot], axis=0)
            norm["MAUT"] = sum(norm[f"n_{k}"] * bobot[k] for k in bobot)
            norm["Rank WP"] = norm["WP"].rank(ascending=False).astype(int)
            norm["Rank MAUT"] = norm["MAUT"].rank(ascending=False).astype(int)
            tab1, tab2 = st.tabs(["📊 Tabel Hasil", "📈 Visualisasi"])
            with tab1:
                st.dataframe(norm[["nama", "WP", "Rank WP", "MAUT", "Rank MAUT"]])
                xlsx = convert_df_to_excel(
                    norm[["nama", "WP", "Rank WP", "MAUT", "Rank MAUT"]]
                )
                st.download_button("⬇️ Unduh Excel", xlsx, "ranking_laptop.xlsx")
            with tab2:
                st.plotly_chart(px.bar(norm, x="nama", y="WP", title="Ranking WP"))
                st.plotly_chart(px.bar(norm, x="nama", y="MAUT", title="Ranking MAUT"))
        except Exception as e:
            st.error(f"Gagal menghitung: {e}")
