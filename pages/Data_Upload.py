import streamlit as st
import pandas as pd
import os

from utils.ui import load_theme, page_header

st.set_page_config(page_title="Data Upload", layout="wide")

load_theme()

page_header(
    "Data Upload",
    "Bring in a fresh CSV dataset and instantly preview the source that powers forecasting, analytics, and reporting.",
    "Ingestion"
)

st.markdown(
    """
    <div class="surface-card">
        <div class="badge-row">
            <span class="badge primary">CSV only</span>
            <span class="badge">Auto-saves to data/sales_data.csv</span>
            <span class="badge">Preview before preprocessing</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload Sales Dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    os.makedirs("data", exist_ok=True)

    df.to_csv(
        "data/sales_data.csv",
        index=False
    )

    st.success("Dataset Uploaded Successfully")

    st.markdown(
        """
        <div class="info-band">
            The uploaded file is now available for preprocessing, EDA, model training, and report generation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(20),
        width="stretch"
    )

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Rows",
        df.shape[0]
    )

    col2.metric(
        "Columns",
        df.shape[1]
    )

    col3.metric(
        "Missing Values",
        df.isnull().sum().sum()
    )

    st.subheader("Dataset Information")

    st.write(df.dtypes)

else:
    st.warning(
        "Please upload a CSV file to activate the full sales intelligence workflow."
    )