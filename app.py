# =====================================================
# VIEW TEMPLATE
# =====================================================

if menu == "Lihat Template":

    df = load_data()

    st.title("📚 Template BO")

    search = st.text_input(
        "🔍 Cari Kode Template"
    )

    # ==========================================
    # SEARCH BERDASARKAN NamaTemplate
    # ==========================================

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

        if len(hasil) == 0:
            st.warning(
                "Kode template tidak ditemukan."
            )
            st.stop()

        row = hasil.iloc[0]

        st.subheader(
            row["NamaTemplate"]
        )

        st.text_area(
            "Isi Template",
            value=row["IsiTemplate"],
            height=300
        )

        st.stop()

    # ==========================================
    # MODE NORMAL (DROPDOWN)
    # ==========================================

    kategori_list = sorted(
        df["Kategori"]
        .dropna()
        .unique()
        .tolist()
    )

    if len(kategori_list) == 0:
        st.warning(
            "Belum ada data."
        )
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

    st.subheader(template)

    st.text_area(
        "Isi Template",
        value=row["IsiTemplate"],
        height=300
    )
