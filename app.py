import streamlit as st
import json
from pathlib import Path

DATA_FILE = "templates.json"

st.set_page_config(page_title="Template BO", layout="wide")

def load_data():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"Gangguan": {}, "Keluhan": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

st.sidebar.title("📚 TEMPLATE BO")

menu = st.sidebar.radio(
    "Menu",
    ["Lihat Template", "Kelola Template"]
)

if menu == "Lihat Template":
    kategori = st.selectbox("Kategori", list(data.keys()))

    if data[kategori]:
        submenu = st.selectbox("Submenu", list(data[kategori].keys()))

        if data[kategori][submenu]:
            nama_template = st.selectbox(
                "Template",
                list(data[kategori][submenu].keys())
            )

            isi = data[kategori][submenu][nama_template]

            st.subheader(nama_template)
            st.text_area("Isi Template", value=isi, height=250)

            st.code(isi)

    else:
        st.warning("Belum ada template.")

else:
    st.header("⚙️ Kelola Template")

    aksi = st.radio(
        "Pilih Aksi",
        ["Tambah", "Edit", "Hapus"]
    )

    if aksi == "Tambah":
        kategori = st.selectbox(
            "Kategori",
            ["Gangguan", "Keluhan"]
        )

        submenu = st.text_input("Nama Submenu")
        nama_template = st.text_input("Nama Template")
        isi_template = st.text_area("Isi Template", height=200)

        if st.button("💾 Simpan"):
            data.setdefault(kategori, {})
            data[kategori].setdefault(submenu, {})
            data[kategori][submenu][nama_template] = isi_template
            save_data(data)
            st.success("Template berhasil disimpan.")

    elif aksi == "Edit":
        kategori = st.selectbox("Kategori", list(data.keys()))

        if data[kategori]:
            submenu = st.selectbox(
                "Submenu",
                list(data[kategori].keys())
            )

            nama_template = st.selectbox(
                "Template",
                list(data[kategori][submenu].keys())
            )

            isi_baru = st.text_area(
                "Edit Template",
                value=data[kategori][submenu][nama_template],
                height=250
            )

            if st.button("💾 Update"):
                data[kategori][submenu][nama_template] = isi_baru
                save_data(data)
                st.success("Template berhasil diperbarui.")

    elif aksi == "Hapus":
        kategori = st.selectbox("Kategori", list(data.keys()))

        if data[kategori]:
            submenu = st.selectbox(
                "Submenu",
                list(data[kategori].keys())
            )

            nama_template = st.selectbox(
                "Template",
                list(data[kategori][submenu].keys())
            )

            if st.button("🗑️ Hapus"):
                del data[kategori][submenu][nama_template]

                if not data[kategori][submenu]:
                    del data[kategori][submenu]

                save_data(data)
                st.success("Template berhasil dihapus.")
