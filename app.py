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
# CONNECT GOOGLE SHEET
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


# =====================================================
# HEADER
# =====================================================

st.title("📚 Template BO")

df = load_data()

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
# VALIDASI DATA
# =====================================================

if len(df) == 0:

    st.warning(
        "Template tidak ditemukan."
    )

    st.stop()

# =====================================================
# KATEGORI
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
# SUBMENU
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
# TEMPLATE
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

isi_template = row["IsiTemplate"]

# =====================================================
# TAMPILKAN TEMPLATE
# =====================================================

st.divider()

st.header(template)

edited_text = st.text_area(
    "Isi Template",
    value=isi_template,
    height=350
)

# =====================================================
# COPY BUTTON
# =====================================================

copy_html = f"""
<div style="margin-top:10px;">
<textarea id="copytext" style="display:none;">{edited_text}</textarea>

<button
style="
background:#16a34a;
color:white;
border:none;
padding:10px 20px;
border-radius:8px;
cursor:pointer;
font-weight:bold;
"
onclick="
navigator.clipboard.writeText(
document.getElementById('copytext').value
);
alert('Template berhasil dicopy');
">
📋 Copy Template
</button>
</div>
"""

components.html(
    copy_html,
    height=70
)

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Template BO - Data sumber Google Sheets"
)
