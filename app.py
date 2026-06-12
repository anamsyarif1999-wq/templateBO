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
        "1vhdIpJ9esIMPVuGRbvU4uU6qCrTQ8D8bpLOA_vH3yhg"
    )

    worksheet = spreadsheet.worksheet("Template")

    return worksheet

sheet = connect_sheet()

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(ttl=5)
def load_data():

    data = sheet.get_all_records()

    if len(data) == 0:
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
# VIEW TEMPLATE
# =====================================================

if menu == "Lihat Template":

    df = load_data()

    st.title("📚 Template BO")

    search = st.text_input(
        "🔍 Cari Template"
    )

    if search:

        df = df[
            df.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    kategori_list = sorted(
        df["Kategori"].dropna().unique().tolist()
    )

    if len(kategori_list) == 0:
        st.warning("Belum ada data.")
        st.stop()

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
        .tolist()
    )

    template = st.selectbox(
        "Template",
        template_list
    )

    row = df_submenu[
        df_submenu["NamaTemplate"] == template
    ].iloc[0]

    isi = row["IsiTemplate"]

    st.subheader(template)

    st.text_area(
        "Isi Template",
        isi,
        height=250
    )

    st.code(isi)

# =====================================================
# MANAGE TEMPLATE
# =====================================================

if menu == "Kelola Template":

    st.title("⚙️ Kelola Template")

    df = load_data()

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Simpan Perubahan",
            use_container_width=True
        ):

            sheet.clear()

            sheet.update(
                [
                    edited_df.columns.tolist()
                ]
                +
                edited_df.values.tolist()
            )

            st.cache_data.clear()

            st.success(
                "Data berhasil disimpan ke Google Sheets"
            )

            st.rerun()

    with col2:

        if st.button(
            "🔄 Refresh",
            use_container_width=True
        ):

            st.cache_data.clear()
            st.rerun()

    st.info(
        """
        Cara penggunaan:

        ➕ Tambah template = tambah baris baru

        ✏️ Edit template = ubah langsung pada tabel

        🗑️ Hapus template = hapus baris

        💾 Simpan Perubahan = simpan ke Google Sheets
        """
    )
