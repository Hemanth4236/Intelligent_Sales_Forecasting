import streamlit as st
import pandas as pd
import plotly.express as px
import os

from models.inventory import inventory_analysis
from utils.ui import load_theme, page_header, theme_plotly

st.set_page_config(
    page_title="Inventory Optimization",
    layout="wide"
)

load_theme()

page_header(
    "Inventory Optimization",
    "Highlight healthy stock, reorder pressure, and overstock risk with a clean operational snapshot.",
    "Stock control"
)

file_path = "data/processed_data.csv"

if not os.path.exists(file_path):
    st.error("Processed dataset not found.")

else:

    df = pd.read_csv(file_path)

    st.markdown(
        """
        <div class="surface-card">
            Inventory status is derived from the current stock position against the reorder threshold for each product.
        </div>
        """,
        unsafe_allow_html=True,
    )

    required_cols = [
        "Product_Name",
        "Inventory_Level",
        "Reorder_Point"
    ]

    missing_cols = [
        col for col in required_cols
        if col not in df.columns
    ]

    if missing_cols:
        st.error(
            f"Missing columns: {missing_cols}"
        )

    else:

        result = inventory_analysis(df)

        healthy = len(
            result[
                result["Inventory_Status"] == "Healthy"
            ]
        )

        reorder = len(
            result[
                result["Inventory_Status"] == "Reorder Required"
            ]
        )

        overstock = len(
            result[
                result["Inventory_Status"] == "Overstock"
            ]
        )

        col1,col2,col3 = st.columns(3)

        col1.metric(
            "Healthy Products",
            healthy
        )

        col2.metric(
            "Reorder Required",
            reorder
        )

        col3.metric(
            "Overstock Items",
            overstock
        )

        st.markdown("---")

        pie_df = pd.DataFrame({
            "Status":[
                "Healthy",
                "Reorder Required",
                "Overstock"
            ],
            "Count":[
                healthy,
                reorder,
                overstock
            ]
        })

        fig = px.pie(
            pie_df,
            names="Status",
            values="Count",
            hole=0.5,
            title="Inventory Health"
        )

        fig = theme_plotly(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.subheader(
            "Inventory Details"
        )

        st.dataframe(
            result[
                [
                    "Product_Name",
                    "Inventory_Level",
                    "Reorder_Point",
                    "Inventory_Status"
                ]
            ],
            width="stretch"
        )