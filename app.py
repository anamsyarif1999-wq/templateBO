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
# GOOGLE SHEET
# =====================================================

SPREADSHEET_ID = "1vhdIpJ9esIMPVuGRbvU4uU6qCrTQ8D8bpLOA_vH3yhg"
WORKSHEET_NAME = "Template"

# =====================================================
# CONNECT
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
# SAVE DATA
# =====================================================

def save_dataframe(df):

    sheet.clear()

    sheet.update(
        [df.columns.tolist()]
        +
        df.fillna("").values.tolist()
    )

    st.cache_data.clear()

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

    search = st.text_input(
        "🔍 Cari Template"
    )

    if search:

        mask = df.astype(str).apply(
            lambda x:
            x.str.contains(
                search,
                case=False,
                na=False
            )
        ).any(axis=1)

        df = df[mask]

    if len(df) == 0:

        st.warning(
            "Template tidak ditemukan."
        )

        st.stop()

    kategori_list = sorted(
        df["Kategori"]
        .dropna()
        .unique()
        .tolist()
    )

    kategori = st.selectbox(
        "Kategori",
        kategori_list
    )

    df1 = df[
        df["Kategori"] == kategori
    ]

    submenu_list = sorted(
        df1["Submenu"]
        .dropna()
        .unique()
        .tolist()
    )

    submenu = st.selectbox(
        "Submenu",
        submenu_list
    )

    df2 = df1[
        df1["Submenu"] == submenu
    ]

    template_list = sorted(
        df2["NamaTemplate"]
        .tolist()
    )

    template = st.selectbox(
        "Template",
        template_list
    )

    row = df2[
        df2["NamaTemplate"] == template
    ].iloc[0]

    isi = row["IsiTemplate"]

    st.markdown("---")

    st.subheader(template)

    st.text_area(
        "Isi Template",
        value=isi,
        height=300,
        disabled=True
    )

    st.download_button(
        "📥 Download TXT",
        isi,
        file_name=f"{template}.txt"
    )

# =====================================================
# KELOLA TEMPLATE
# =====================================================

if menu == "Kelola Template":

    st.title("⚙️ Kelola Template")

    df = load_data()

    tab1, tab2 = st.tabs(
        [
            "Tambah Template",
            "Edit Data"
        ]
    )

    # ==========================================
    # TAB TAMBAH
    # ==========================================

    with tab1:

        kategori = st.text_input(
            "Kategori"
        )

        submenu = st.text_input(
            "Submenu"
        )

        nama = st.text_input(
            "Nama Template"
        )

        isi = st.text_area(
            "Isi Template",
            height=250
        )

        if st.button(
            "➕ Tambah Template"
        ):

            if (
                kategori
                and submenu
                and nama
                and isi
            ):

                new_row = pd.DataFrame([
                    {
                        "Kategori": kategori,
                        "Submenu": submenu,
                        "NamaTemplate": nama,
                        "IsiTemplate": isi
                    }
                ])

                df = pd.concat(
                    [df, new_row],
                    ignore_index=True
                )

                save_dataframe(df)

                st.success(
                    "Template berhasil ditambahkan"
                )

                st.rerun()

            else:

                st.warning(
                    "Lengkapi semua data."
                )

    # ==========================================
    # TAB EDIT
    # ==========================================

    with tab2:

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

                save_dataframe(
                    edited_df
                )

                st.success(
                    "Perubahan berhasil disimpan"
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

            ➕ Tambah baris = tambah template

            ✏️ Edit langsung di tabel

            🗑️ Hapus baris = hapus template

            💾 Simpan Perubahan untuk menyimpan ke Google Sheets
            """
        )
