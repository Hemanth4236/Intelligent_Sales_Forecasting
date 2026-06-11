import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.ui import load_theme, page_header, theme_plotly

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

load_theme()

page_header(
    "Executive Dashboard",
    "A polished command center for revenue, orders, inventory, and category performance.",
    "Live performance"
)

file_path = "data/processed_data.csv"

if not os.path.exists(file_path):
    st.error("Processed dataset not found.")

else:

    df = pd.read_csv(file_path)

    st.markdown(
        """
        <div class="info-band">
            Snapshot values below are pulled from the processed dataset and update whenever the file changes.
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_revenue = df[
        "Sales_Revenue"
    ].sum()

    total_orders = len(df)

    avg_sales = round(
        df["Sales_Revenue"].mean(),
        2
    )

    inventory_cost = (
        df["Inventory_Level"].sum()
        if "Inventory_Level" in df.columns
        else 0
    )

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "Revenue",
        f"₹ {total_revenue:,.0f}"
    )

    col2.metric(
        "Orders",
        total_orders
    )

    col3.metric(
        "Average Sales",
        f"₹ {avg_sales:,.0f}"
    )

    col4.metric(
        "Inventory",
        inventory_cost
    )

    st.markdown("---")

    left,right = st.columns(2)

    with left:

        if "Date" in df.columns:

            trend = px.line(
                df,
                x="Date",
                y="Sales_Revenue",
                title="Revenue Trend"
            )

            trend = theme_plotly(trend)

            st.plotly_chart(
                trend,
                width="stretch"
            )

    with right:

        if "Category" in df.columns:

            category = px.bar(
                df.groupby(
                    "Category"
                )[
                    "Sales_Revenue"
                ].sum().reset_index(),
                x="Category",
                y="Sales_Revenue",
                color="Category",
                title="Category Revenue"
            )

            category = theme_plotly(category)

            st.plotly_chart(
                category,
                width="stretch"
            )

    st.markdown("---")

    bottom1,bottom2 = st.columns(2)

    with bottom1:

        if "Region" in df.columns:

            region = px.pie(
                df,
                names="Region",
                values="Sales_Revenue",
                title="Region Sales"
            )

            region = theme_plotly(region)

            st.plotly_chart(
                region,
                width="stretch"
            )

    with bottom2:

        top_products = (
            df.groupby(
                "Product_Name"
            )[
                "Sales_Revenue"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            top_products,
            x="Product_Name",
            y="Sales_Revenue",
            title="Top Products"
        )

        fig = theme_plotly(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    st.markdown(
        """
        <div class="surface-card">
            <strong>AI Business Insights</strong>
            <p style="margin:0.6rem 0 0; color:#bfd0ea; line-height:1.7;">
                Sales momentum is healthy, inventory pressure should be watched on lower-stock items,
                and the strongest categories should receive the next round of promotional focus.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )