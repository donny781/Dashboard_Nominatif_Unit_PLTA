import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

st.set_page_config(page_title="Dashboard Nominatif Unit PLTA", layout="wide")

# ======================
# LOGIN
# ======================

def login():
    st.markdown("## 🔐 Login Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "plta123":
            st.session_state["login"] = True
        else:
            st.error("Username atau Password salah")

if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
    st.stop()

# ======================
# DASHBOARD
# ======================

st.title("📊 Dashboard Nominatif Unit PLTA")
st.markdown("Sistem Monitoring & Export Laporan PDF")

uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # METRIC
    st.subheader("Ringkasan Data")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Data", len(df))
    col2.metric("Total Kolom", len(df.columns))
    col3.metric("Total Data Kosong", df.isnull().sum().sum())

    # FILTER
    st.subheader("Filter Data")
    selected_column = st.selectbox("Pilih Kolom", df.columns)

    if df[selected_column].dtype == "object":
        selected_values = st.multiselect(
            "Pilih Nilai",
            df[selected_column].dropna().unique(),
            default=df[selected_column].dropna().unique()
        )
        filtered_df = df[df[selected_column].isin(selected_values)]
    else:
        min_val = float(df[selected_column].min())
        max_val = float(df[selected_column].max())
        selected_range = st.slider("Pilih Rentang", min_val, max_val, (min_val, max_val))
        filtered_df = df[
            (df[selected_column] >= selected_range[0]) &
            (df[selected_column] <= selected_range[1])
        ]

    # TABEL
    st.subheader("Data Setelah Filter")
    st.dataframe(filtered_df, use_container_width=True)

    # DOWNLOAD CSV
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Data (CSV)",
        csv,
        "data_filtered.csv",
        "text/csv"
    )

    # ======================
    # EXPORT PDF
    # ======================

    def generate_pdf(dataframe):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Laporan Data Nominatif Unit PLTA", styles["Title"]))
        elements.append(Spacer(1, 0.5 * inch))

        data = [dataframe.columns.tolist()] + dataframe.values.tolist()

        table = Table(data)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ])

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer

    pdf_file = generate_pdf(filtered_df.head(50))

    st.download_button(
        label="📄 Download Laporan PDF",
        data=pdf_file,
        file_name="Laporan_Nominatif_PLTA.pdf",
        mime="application/pdf"
    )

    # GRAFIK
    st.subheader("Grafik Distribusi")
    fig = plt.figure()
    filtered_df[selected_column].value_counts().head(10).plot(kind="bar")
    st.pyplot(fig)

else:
    st.info("Silakan upload file Excel untuk memulai dashboard.")
# ======================
# DASHBOARD UTAMA
# ======================

st.title("📊 Dashboard Nominatif Unit PLTA")
st.markdown("Sistem Monitoring Data Nominatif")

uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # METRIC
    st.subheader("Ringkasan Data")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Data", len(df))
    col2.metric("Total Kolom", len(df.columns))
    col3.metric("Total Data Kosong", df.isnull().sum().sum())

    # FILTER
    st.subheader("Filter Data")
    selected_column = st.selectbox("Pilih Kolom", df.columns)

    if df[selected_column].dtype == "object":
        selected_values = st.multiselect(
            "Pilih Nilai",
            df[selected_column].dropna().unique(),
            default=df[selected_column].dropna().unique()
        )
        filtered_df = df[df[selected_column].isin(selected_values)]
    else:
        min_val = float(df[selected_column].min())
        max_val = float(df[selected_column].max())
        selected_range = st.slider(
            "Pilih Rentang",
            min_val,
            max_val,
            (min_val, max_val)
        )
        filtered_df = df[
            (df[selected_column] >= selected_range[0]) &
            (df[selected_column] <= selected_range[1])
        ]

    # TABEL
    st.subheader("Data Setelah Filter")
    st.dataframe(filtered_df, use_container_width=True)

    # DOWNLOAD
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Data (CSV)",
        csv,# ===== EXPORT PDF =====
def generate_pdf(dataframe):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("Laporan Data Nominatif Unit PLTA", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    data = [dataframe.columns.tolist()] + dataframe.values.tolist()
    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ])

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf_file = generate_pdf(filtered_df.head(50))  # maksimal 50 baris agar tidak terlalu panjang

st.download_button(
    label="Download Laporan PDF",
    data=pdf_file,
    file_name="Laporan_Nominatif_PLTA.pdf",
    mime="application/pdf"
        )
        "data_filtered.csv",
        "text/csv"
    )

    # GRAFIK
    st.subheader("Grafik Distribusi")
    fig = plt.figure()
    filtered_df[selected_column].value_counts().head(10).plot(kind="bar")
    st.pyplot(fig)

else:
    st.info("Silakan upload file Excel untuk memulai dashboard.")
