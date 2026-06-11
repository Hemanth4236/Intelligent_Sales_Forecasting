import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.ui import load_theme, page_header, theme_plotly

st.set_page_config(
    page_title="EDA Analysis",
    layout="wide"
)

load_theme()

page_header(
    "Exploratory Data Analysis",
    "Explore sales behavior with colorful trend, category, region, and correlation views.",
    "Insight discovery"
)

file_path = "data/processed_data.csv"

if not os.path.exists(file_path):

    st.error(
        "Preprocessed dataset not found."
    )

else:

    df = pd.read_csv(file_path)

    numeric_df = df.select_dtypes(include="number")

    sales_df = df.copy()

    if "Date" in sales_df.columns:
        sales_df["Date"] = pd.to_datetime(
            sales_df["Date"],
            errors="coerce"
        )

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric("Rows", len(df))
    metric_col2.metric("Numeric columns", len(numeric_df.columns))
    metric_col3.metric("Missing values", int(df.isnull().sum().sum()))

    st.markdown("---")

    st.subheader("Dataset Overview")

    st.dataframe(
        df.head(),
        width="stretch"
    )

    tab1,tab2,tab3 = st.tabs(
        [
            "Sales Trend",
            "Category Analysis",
            "Region Analysis"
        ]
    )

    with tab1:

        if "Date" in df.columns and "Sales_Revenue" in df.columns:

            cleaned_sales_df = sales_df.dropna(
                subset=["Date", "Sales_Revenue"]
            ).sort_values("Date")

            daily_sales = cleaned_sales_df.groupby(
                pd.Grouper(key="Date", freq="D")
            )["Sales_Revenue"].sum().reset_index()

            weekly_sales = cleaned_sales_df.groupby(
                pd.Grouper(key="Date", freq="W")
            )["Sales_Revenue"].sum().reset_index()

            monthly_sales = cleaned_sales_df.groupby(
                pd.Grouper(key="Date", freq="ME")
            )["Sales_Revenue"].sum().reset_index()

            fig = px.line(
                daily_sales,
                x="Date",
                y="Sales_Revenue",
                title="Daily Sales Trend"
            )

            fig = theme_plotly(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )

            weekly_fig = px.line(
                weekly_sales,
                x="Date",
                y="Sales_Revenue",
                markers=True,
                title="Weekly Sales Trend"
            )

            weekly_fig = theme_plotly(weekly_fig)

            st.plotly_chart(
                weekly_fig,
                width="stretch"
            )

            monthly_fig = px.line(
                monthly_sales,
                x="Date",
                y="Sales_Revenue",
                markers=True,
                title="Monthly Sales Trend"
            )

            monthly_fig = theme_plotly(monthly_fig)

            st.plotly_chart(
                monthly_fig,
                width="stretch"
            )

    with tab2:

        if "Category" in df.columns:

            fig = px.bar(
                df.groupby("Category")[
                    "Sales_Revenue"
                ].sum().reset_index(),
                x="Category",
                y="Sales_Revenue",
                color="Category",
                title="Category Sales"
            )

            fig = theme_plotly(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )

    with tab3:

        if "Region" in df.columns:

            fig = px.pie(
                df,
                names="Region",
                values="Sales_Revenue",
                title="Region Wise Revenue"
            )

            fig = theme_plotly(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )

    st.markdown("---")

    st.subheader("Correlation Analysis")

    if len(numeric_df.columns) > 1:

        corr = numeric_df.corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix"
        )

        fig = theme_plotly(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )