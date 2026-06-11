import streamlit as st
import pandas as pd
import os

from models.preprocessing import preprocess_data
from utils.ui import load_theme, page_header

st.set_page_config(
    page_title="Data Preprocessing",
    layout="wide"
)

load_theme()

page_header(
    "Data Preprocessing",
    "Clean the raw upload, remove noise, and save a refined dataset for forecasting and analysis.",
    "Preparation"
)

file_path = "data/sales_data.csv"

if not os.path.exists(file_path):

    st.error(
        "Upload dataset first."
    )

else:

    df = pd.read_csv(file_path)

    raw_signature = (
        tuple(df.columns),
        len(df),
        int(pd.util.hash_pandas_object(df, index=True).sum()),
    )

    if (
        "processed_df" not in st.session_state
        or st.session_state.get("raw_signature") != raw_signature
    ):
        st.session_state.raw_signature = raw_signature
        st.session_state.processed_df = preprocess_data(df)

    processed_df = st.session_state.processed_df

    st.markdown(
        """
        <div class="surface-card">
            <span class="badge primary">Data quality</span>
            <span class="badge">Missing values, duplicates, and sample rows are shown below.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Raw Dataset")

    st.dataframe(
        df.head(),
        width="stretch"
    )

    st.caption("Raw dataset is the original file saved at data/sales_data.csv.")

    st.markdown("---")

    col1,col2,col3 = st.columns(3)

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    col1.metric(
        "Missing Values",
        missing
    )

    col2.metric(
        "Duplicate Rows",
        duplicates
    )

    col3.metric(
        "Total Records",
        len(df)
    )

    st.markdown("---")

    action_col1, action_col2 = st.columns(2)

    if action_col1.button("Remove Missing Values"):
        st.session_state.processed_df = processed_df.dropna()
        processed_df = st.session_state.processed_df
        st.success("Missing values removed from the working dataset.")

    if action_col2.button("Remove Duplicates"):
        st.session_state.processed_df = processed_df.drop_duplicates()
        processed_df = st.session_state.processed_df
        st.success("Duplicate rows removed from the working dataset.")

    st.subheader("Processed Dataset")

    st.dataframe(
        processed_df.head(),
        width="stretch"
    )

    os.makedirs(
        "data",
        exist_ok=True
    )

    processed_df.to_csv(
        "data/processed_data.csv",
        index=False
    )

    st.success(
        "Processed data saved to data/processed_data.csv"
    )