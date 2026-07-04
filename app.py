import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="BATMAN",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# GOOGLE SHEET
# =====================================================

SPREADSHEET_ID = "1vhdIpJ9esIMPVuGRbvU4uU6qCrTQ8D8bpLOA_vH3yhg"
WORKSHEET_NAME = "Template"

# =====================================================
# CONNECT SHEET
# =====================================================

@st.cache_resource
def connect_sheet():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    worksheet = spreadsheet.worksheet(
        WORKSHEET_NAME
    )

    return worksheet


sheet = connect_sheet()

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(ttl=10)
def load_data():

    data = sheet.get_all_records()

    if not data:
        return pd.DataFrame(
            columns=[
                "Kategori",
                "Submenu",
                "NamaTemplate",
                "IsiTemplate"
            ]
        )

    return pd.DataFrame(data)

# =====================================================
# COPY BUTTON
# =====================================================

def copy_button(label, text):

    text = str(text).replace("`", "\\`")

    html = f"""
    <button
        onclick="
            navigator.clipboard.writeText(`{text}`);
            this.innerHTML='✅ Tersalin';
            setTimeout(() => {{
                this.innerHTML='{label}';
            }}, 1500);
        "
        style="
            background:#16a34a;
            color:white;
            border:none;
            border-radius:8px;
            padding:10px;
            width:100%;
            cursor:pointer;
            font-weight:bold;
        ">
        {label}
    </button>
    """

    components.html(
        html,
        height=55
    )

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📚 TEMPLATE BO")

menu = st.sidebar.radio(
    "Menu",
    [
        "Lihat Template",
        "Kelola Template"
    ]
)

# =====================================================
# LIHAT TEMPLATE
# =====================================================

if menu == "Lihat Template":

    df = load_data()

    st.title("📚 Template BO")

    if df.empty:
        st.warning("Belum ada data template.")
        st.stop()

    # ============================================
    # SEARCH
    # ============================================

    search = st.text_input(
        "🔍 Cari Kode Template"
    )

    row = None

    if search.strip():

        kode = search.strip().upper()

        hasil = df[
            df["NamaTemplate"]
            .astype(str)
            .str.strip()
            .str.upper()
            == kode
        ]

        if hasil.empty:

            st.warning(
                f"Kode template '{kode}' tidak ditemukan."
            )

            st.stop()

        row = hasil.iloc[0]

    else:

        kategori_list = sorted(
            df["Kategori"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        kategori = st.selectbox(
            "Kategori",
            kategori_list
        )

        df_kategori = df[
            df["Kategori"] == kategori
        ]

        submenu_list = sorted(
            df_kategori["Submenu"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        submenu = st.selectbox(
            "Submenu",
            submenu_list
        )

        df_submenu = df_kategori[
            df_kategori["Submenu"] == submenu
        ]

        template_list = sorted(
            df_submenu["NamaTemplate"]
            .dropna()
            .astype(str)
            .tolist()
        )

        template = st.selectbox(
            "Template",
            template_list
        )

        row = df_submenu[
            df_submenu["NamaTemplate"]
            .astype(str)
            .str.strip()
            == template
        ].iloc[0]

    isi = str(row["IsiTemplate"])

    st.divider()

    st.subheader(
        str(row["NamaTemplate"])
    )

    st.text_area(
        "Isi Template",
        value=isi,
        height=250
    )

    # ============================================
    # COPY TEMPLATE
    # ============================================

    st.markdown("### 📋 Copy Template")

    copy_button(
        "📋 COPY TEMPLATE",
        isi
    )

    st.divider()

    # ============================================
# TEMPLATE CEPAT
# ============================================

st.markdown("### ⚡ Template Cepat")

# =====================================================
# BARIS 1 (GANGGUAN)
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    copy_button(
        "LINKLOSS",
        "Dear Tim NOC SBU, mohon bantuan pengecekan dan penanganan segera terkait gangguan Link Loss yang dialami user. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Mohon tindak lanjut dan update hasil pengecekannya. Terima kasih."
    )

with c2:
    copy_button(
        "DOWN",
        "Dear Tim NOC Ritel Pusat, mohon bantuan pengecekan dan penanganan segera terkait pelaporan gangguan internet down yang dialami user. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Mohon tindak lanjut dan update hasil pengecekannya. Terima kasih."
    )

with c3:
    copy_button(
        "SLOW",
        "Dear Tim NOC Ritel Pusat, mohon bantuan pengecekan dan penanganan segera terkait pelaporan gangguan internet slow yang dialami user. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Mohon tindak lanjut dan update hasil pengecekannya. Terima kasih."
    )

with c4:
    copy_button(
        "INTERMITTEN",
        "Dear Tim NOC Ritel Pusat, mohon bantuan pengecekan dan penanganan segera terkait pelaporan gangguan intermitten yang dialami user. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Mohon tindak lanjut dan update hasil pengecekannya. Terima kasih."
    )

# =====================================================
# BARIS 2 
# =====================================================

c11, c12, c13 = st.columns(3)

with c11:
    copy_button(
        "MUTASI 1",
        "Dikarenakan ada ketidaksesuaian dalam pemilihan Jenis Komplain dan berdasarkan analisis yang kami lakukan. Maka akan kami lakukan pergantian."
    )

with c12:
    copy_button(
        "MUTASI 2",
        "Dikarenakan ada ketidaksesuaian dalam pemilihan Jenis Tiket dan berdasarkan analisis yang kami lakukan. Maka akan kami lakukan pergantian."
    )

with c13:
    copy_button(
        "MUTASI 3",
        "Dikarenakan ada ketidaksesuaian dalam pemilihan Posisi Tiket Komplain dan berdasarkan analisis yang kami lakukan. Maka akan kami lakukan pergantian."
    )

# =====================================================
# BARIS 3
# =====================================================

c8, c9, c10 = st.columns(3)

with c8:
    copy_button(
        "DATA TIDAK DITEMUKAN",
        "data tidak ditemukan"
    )

with c9:
    copy_button(
        "ISOLIR",
        "Isolir"
    )

with c10:
    copy_button(
        "MASIH PERIODE",
        "masih periode penggunaan"
    )

# =====================================================
# BARIS 4
# =====================================================

c5, c6, c7 = st.columns(3)

with c5:
    copy_button(
        "CLOSE ISOLIR",
        "IZIN CLOSE KARENA PELANGGAN INDIKASI ISOLIR. #PERCEPATAN BO."
    )

with c6:
    copy_button(
        "CLOSE NORMAL",
        "IZIN CLOSE KARENA PELANGGAN KONFIRMASI NORMAL."
    )

with c7:
    copy_button(
        "CLOSE OB",
        "IZIN CLOSE KARENA SUDAH DIKONFIRMASI DAN DIEDUKASI TIM OUTBOUND."
    )

# =====================================================
# BARIS 5
# =====================================================

c5, c6, c7 = st.columns(3)

with c5:
    copy_button(
        "ACS NOTIF GAGAL",
        "Dear Tim NOC Ritel Pusat, mohon bantuan pengecekan dan penanganan segera terkait pelaporan gangguan internet xxx  yang dialami user. BO sudah bantu refresh ACS akan tetapi gagal, berikut lampirannya. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Mohon tindak lanjut dan update hasil pengecekannya. Terima kasih."
    )

with c6:
    copy_button(
        "ACS (DEVICE NOT RESPONDING)",
        "Dear Tim Outbound, mohon edukasi menunggu 5 sampai 10 menit karena sudah dibantu reboot device berhasil akan tetapi refresh gagal (DEVICE NOT RESPONDING). Apabila pelanggan konfirmasi normal mutasi ke keluhan lain lain agar tiket dapat di close. Jika pelanggan konfirmasi masih gangguan xxxx, mohon dispose tiket ke NOC Ritel Pusat. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Terima kasih."
    )

with c7:
    copy_button(
        "ACS BERHASIL",
        "Dear Tim Outbound, mohon edukasi mencoba jaringan internetnya karena modem sudah dibantu reboot device berhasil. Apabila pelanggan konfirmasi normal mutasi ke keluhan lain lain agar tiket dapat di close. Jika pelanggan konfirmasi masih gangguan xxxx, mohon dispose tiket ke NOC Ritel Pusat. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Terima kasih."
    )

# =====================================================
# BARIS 5
# =====================================================

c5, c6, c7 = st.columns(3)

with c6:
    copy_button(
        "ACS ID TIDAK DITEMUKAN",
        "Dear Tim NOC Ritel Pusat, mohon bantuan pengecekan dan penanganan segera terkait pelaporan gangguan internet down yang dialami user. Data ID Pel tidak ditemukan pada ACS. Berdasarkan verifikasi, status pembayaran pelanggan lunas dan status layanan pada ICRM+ adalah Unisolir. Mohon tindak lanjut dan update hasil pengecekannya. Terima kasih."
    )

# =====================================================
# KELOLA TEMPLATE
# =====================================================

if menu == "Kelola Template":

    st.title("⚙️ Kelola Template")

    df = load_data()

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Simpan Perubahan",
            use_container_width=True
        ):

            try:

                edited_df = edited_df.fillna("")

                data_save = [
                    edited_df.columns.tolist()
                ]

                data_save.extend(
                    edited_df.values.tolist()
                )

                sheet.clear()

                sheet.update(data_save)

                st.cache_data.clear()

                st.success(
                    "Data berhasil disimpan."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Gagal menyimpan data : {e}"
                )

    with col2:

        if st.button(
            "🔄 Refresh",
            use_container_width=True
        ):

            st.cache_data.clear()
            st.rerun()

    st.info(
        """
➕ Tambah Template = Tambah baris baru

✏️ Edit Template = Ubah langsung pada tabel

🗑️ Hapus Template = Hapus baris

💾 Simpan Perubahan = Simpan ke Google Sheets
        """
    )
