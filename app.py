import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components

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
# CSS
# =====================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    max-width: 1400px;
}

.copy-btn {
    background-color: #16a34a;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    cursor: pointer;
}

.copy-btn:hover {
    background-color: #15803d;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEET CONNECTION
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

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(ttl=60)
def load_data():

    try:

        sheet = connect_sheet()

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

    except Exception as e:

        st.error(f"Gagal membaca Google Sheet: {e}")

        return pd.DataFrame()

# =====================================================
# HEADER
# =====================================================

st.title("📚 Template BO")

st.caption("Template otomatis dari Google Sheets")

# =====================================================
# LOAD
# =====================================================

df = load_data()

if df.empty:
    st.stop()

# =====================================================
# SEARCH
# =====================================================

search = st.text_input(
    "🔍 Cari Template"
)

if search:

    mask = df.astype(str).apply(
        lambda x: x.str.contains(
            search,
            case=False,
            na=False
        )
    ).any(axis=1)

    df = df[mask]

# =====================================================
# VALIDASI
# =====================================================

if len(df) == 0:

    st.warning(
        "Template tidak ditemukan."
    )

    st.stop()

# =====================================================
# FILTER KATEGORI
# =====================================================

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

df_kategori = df[
    df["Kategori"] == kategori
]

# =====================================================
# FILTER SUBMENU
# =====================================================

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

# =====================================================
# FILTER TEMPLATE
# =====================================================

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

isi_template = str(row["IsiTemplate"])

# =====================================================
# TAMPILKAN TEMPLATE
# =====================================================

st.divider()

st.header(template)

edited_text = st.text_area(
    "Isi Template",
    value=isi_template,
    height=300
)

# =====================================================
# COPY BUTTON
# =====================================================

copy_html = f"""
<textarea id="copyText" style="display:none;">{edited_text}</textarea>

<button
class="copy-btn"
onclick="
navigator.clipboard.writeText(
document.getElementById('copyText').value
);
alert('Template berhasil dicopy');
">
📋 Copy Template
</button>
"""

components.html(
    copy_html,
    height=60
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Template BO - Data sumber Google Sheets"
)
