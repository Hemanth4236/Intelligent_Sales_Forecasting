import streamlit as st
import pandas as pd
import os
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from utils.ui import load_theme, page_header

st.set_page_config(
    page_title="Reports",
    layout="wide"
)

load_theme()


def prepare_report_df(df):

    report_df = df.copy()

    if "Date" in report_df.columns:
        date_values = pd.to_datetime(report_df["Date"], errors="coerce")
        formatted_dates = date_values.dt.strftime("%Y-%m-%d")
        formatted_dates = formatted_dates.fillna(report_df["Date"].astype(str))
        report_df["Date"] = "'" + formatted_dates.astype(str)

    datetime_columns = report_df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns

    for column in datetime_columns:
        report_df[column] = pd.to_datetime(report_df[column], errors="coerce").dt.strftime("%Y-%m-%d")

    return report_df


def build_pdf_report(df, report_type):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=18,
        leftMargin=18,
        topMargin=18,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"{report_type}", styles["Title"]))
    elements.append(Paragraph("Processed sales dataset export", styles["Normal"]))
    elements.append(Spacer(1, 12))

    table_data = [list(df.columns)] + df.astype(str).values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fb")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return buffer.getvalue()

page_header(
    "Reports",
    "Create a polished export view for sales, inventory, or forecast reporting needs.",
    "Delivery"
)

file_path = "data/processed_data.csv"

if not os.path.exists(file_path):
    st.error("Processed dataset not found.")

else:

    df = pd.read_csv(file_path)
    export_df = prepare_report_df(df)

    st.markdown(
        """
        <div class="surface-card">
            Choose a report style, preview the latest dataset, and download a clean CSV package for stakeholders.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(
        "Generate Business Reports"
    )

    report_type = st.selectbox(
        "Select Report",
        [
            "Sales Report",
            "Inventory Report",
            "Forecast Report"
        ]
    )

    st.write(
        f"Selected: {report_type}"
    )

    st.markdown("---")

    csv = export_df.to_csv(
        index=False
    ).encode("utf-8")

    pdf = build_pdf_report(
        export_df,
        report_type
    )

    download_col1, download_col2 = st.columns(2)

    with download_col1:
        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="report.csv",
            mime="text/csv"
        )

    with download_col2:
        st.download_button(
            label="⬇ Download PDF",
            data=pdf,
            file_name="report.pdf",
            mime="application/pdf"
        )

    st.subheader(
        "Preview"
    )

    st.dataframe(
        export_df.head(20),
        width="stretch"
    )