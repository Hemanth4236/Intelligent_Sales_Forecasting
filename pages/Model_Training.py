import streamlit as st
import pandas as pd
import os
import plotly.express as px

from models.training import train_model
from utils.ui import load_theme, page_header

st.set_page_config(
    page_title="Model Training",
    layout="wide"
)

load_theme()

page_header(
    "Model Training",
    "Train a forecasting model on the cleaned dataset and review the evaluation metrics in one place.",
    "Model lab"
)

file_path = "data/processed_data.csv"

if not os.path.exists(file_path):

    st.error(
        "Preprocessed dataset not found."
    )

else:

    df = pd.read_csv(file_path)

    st.markdown(
        """
        <div class="surface-card">
            Select the model, train it on numeric features, and compare the resulting error metrics.
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_col, action_col = st.columns([2, 1])

    with model_col:
        model_name = st.selectbox(
            "Model",
            [
                "Random Forest",
                "Linear Regression"
            ]
        )

    with action_col:
        st.write("")
        train_pressed = st.button("Train Model")

    st.markdown(
        f"""
        <div class="info-band">
            <strong>Selected model:</strong> {model_name} | the trained estimator is saved to models/sales_model.pkl.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if train_pressed:

        with st.spinner(
            "Training model..."
        ):

            model, mae, rmse, r2, results_df, feature_importance = train_model(df, model_name)

        st.success(
            f"{model_name} trained successfully"
        )

        col1,col2,col3 = st.columns(3)

        col1.metric(
            "MAE",
            round(mae,2)
        )

        col2.metric(
            "RMSE",
            round(rmse,2)
        )

        col3.metric(
            "R² Score",
            round(r2,2)
        )

        st.markdown(
            """
            <div class="surface-card">
                The metrics above reflect the latest validation split. Lower MAE and RMSE indicate tighter predictions,
                while a stronger R² suggests the model explains more of the sales variation.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("Training Results Table")

        display_df = results_df.copy().reset_index(drop=True)
        display_df["Prediction_Error"] = display_df["Actual"] - display_df["Predicted"]

        st.dataframe(
            display_df.style.format(
                {
                    "Actual": "{:,.2f}",
                    "Predicted": "{:,.2f}",
                    "Error": "{:,.2f}",
                    "Absolute_Error": "{:,.2f}",
                    "Prediction_Error": "{:,.2f}",
                }
            ),
            width="stretch",
        )

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            comparison_df = display_df.head(20).reset_index().rename(columns={"index": "Sample"})
            comparison_fig = px.line(
                comparison_df,
                x="Sample",
                y=["Actual", "Predicted"],
                markers=True,
                title="Actual vs Predicted Sales",
            )
            comparison_fig.update_layout(legend_title_text="Series")
            st.plotly_chart(comparison_fig, use_container_width=True)

        with chart_col2:
            residual_fig = px.bar(
                display_df.head(20).reset_index().rename(columns={"index": "Sample"}),
                x="Sample",
                y="Error",
                title="Prediction Error by Sample",
            )
            st.plotly_chart(residual_fig, use_container_width=True)

        if feature_importance is not None and not feature_importance.empty:
            st.subheader("Feature Importance")

            feature_fig = px.bar(
                feature_importance.head(10),
                x="Importance",
                y="Feature",
                orientation="h",
                title="Top Training Features",
            )
            feature_fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(feature_fig, use_container_width=True)