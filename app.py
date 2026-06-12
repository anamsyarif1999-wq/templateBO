import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Template BO",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# GOOGLE SHEETS CONNECTION
# =====================================================

SPREADSHEET_ID = "1vhdIpJ9esIMPVuGRbvU4uU6qCrTQ8D8bpLOA_vH3yhg"
WORKSHEET_NAME = "Template"

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

    # =================================================
    # SEARCH TEMPLATE
    # =================================================

    search = st.text_input(
        "🔍 Cari Kode Template"
    )

    # =================================================
    # MODE SEARCH
    # =================================================

    if search.strip():

        hasil = df[
            df["NamaTemplate"]
            .astype(str)
            .str.strip()
            .str.contains(
                search.strip(),
                case=False,
                na=False
            )
        ]

        if hasil.empty:
            st.warning(
                "Kode template tidak ditemukan."
            )
            st.stop()

        row = hasil.iloc[0]

        st.divider()

        st.subheader(
            str(row["NamaTemplate"])
        )

        st.text_area(
            "Isi Template",
            value=str(row["IsiTemplate"]),
            height=300
        )

        st.stop()

    # =================================================
    # MODE DROPDOWN
    # =================================================

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
        df_submenu["NamaTemplate"] == template
    ].iloc[0]

    st.divider()

    st.subheader(
        str(row["NamaTemplate"])
    )

    st.text_area(
        "Isi Template",
        value=str(row["IsiTemplate"]),
        height=300
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

                data_to_save = [
                    edited_df.columns.tolist()
                ]

                data_to_save.extend(
                    edited_df.values.tolist()
                )

                sheet.clear()

                sheet.update(
                    data_to_save
                )

                st.cache_data.clear()

                st.success(
                    "Data berhasil disimpan ke Google Sheets."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Gagal menyimpan data: {e}"
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
➕ Tambah template = tambah baris baru

✏️ Edit template = ubah langsung pada tabel

🗑️ Hapus template = hapus baris

💾 Simpan Perubahan = simpan ke Google Sheets
"""
    )
