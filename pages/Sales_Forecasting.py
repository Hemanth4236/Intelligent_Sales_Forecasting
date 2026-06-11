import streamlit as st
import pandas as pd
import plotly.express as px
import os

from models.forecasting import sales_forecast
from utils.ui import load_theme, page_header, theme_plotly

st.set_page_config(
    page_title="Sales Forecasting",
    layout="wide"
)

load_theme()

page_header(
    "Sales Forecasting",
    "Project future demand with a clean forecast horizon control and an elegant line forecast display.",
    "Prediction"
)

file_path = "data/processed_data.csv"

if not os.path.exists(file_path):

    st.error(
        "Processed dataset not found."
    )

else:

    df = pd.read_csv(file_path)

    st.markdown(
        """
        <div class="surface-card">
            Use the forecast horizon to simulate demand over the next 30, 60, 90, or 180 days.
        </div>
        """,
        unsafe_allow_html=True,
    )

    horizon_col, action_col = st.columns([2, 1])

    with horizon_col:
        days = st.selectbox(
            "Forecast Horizon",
            [
                30,
                60,
                90,
                180
            ]
        )

    with action_col:
        st.write("")
        generate_pressed = st.button("Generate Forecast")

    if generate_pressed:

        with st.spinner(
            "Generating Forecast..."
        ):

            forecast = sales_forecast(
                df,
                days
            )

        st.success(
            "Forecast generated successfully"
        )

        predicted_revenue = round(
            forecast["yhat"]
            .tail(days)
            .sum(),
            2
        )

        avg_daily = round(
            forecast["yhat"]
            .tail(days)
            .mean(),
            2
        )

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        metric_col1.metric("Predicted Revenue", f"₹ {predicted_revenue:,.0f}")
        metric_col2.metric("Average Daily Forecast", f"₹ {avg_daily:,.0f}")
        metric_col3.metric("Forecast Horizon", f"{days} days")

        fig = px.line(
            forecast,
            x="ds",
            y="yhat",
            title=f"{days} Day Sales Forecast"
        )

        fig = theme_plotly(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.subheader(
            "Forecast Data"
        )

        st.dataframe(
            forecast[
                [
                    "ds",
                    "yhat",
                    "yhat_lower",
                    "yhat_upper"
                ]
            ].tail(days),
            width="stretch"
        )

        st.markdown(
            """
            <div class="info-band">
                Forecast bands are shown in the table below so the optimistic and conservative paths can be reviewed together.
            </div>
            """,
            unsafe_allow_html=True,
        )