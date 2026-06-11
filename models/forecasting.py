import importlib
import importlib.util

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def sales_forecast(df, days=90):

    data = df[
        [
            "Date",
            "Sales_Revenue"
        ]
    ].copy()

    data.columns = [
        "ds",
        "y"
    ]

    data["ds"] = pd.to_datetime(data["ds"], errors="coerce")
    data["y"] = pd.to_numeric(data["y"], errors="coerce")
    data = data.dropna().sort_values("ds")

    if data.empty:
        raise ValueError("No valid sales data found for forecasting.")

    if importlib.util.find_spec("prophet") is not None:
        Prophet = importlib.import_module("prophet").Prophet

        model = Prophet()
        model.fit(data)

        future = model.make_future_dataframe(periods=days)
        forecast = model.predict(future)

        return forecast

    history = data.reset_index(drop=True).copy()
    history["time_index"] = np.arange(len(history))

    model = LinearRegression()
    model.fit(history[["time_index"]], history["y"])

    forecast_index = pd.DataFrame(
        {"time_index": np.arange(len(history) + days)}
    )
    forecast_dates = pd.date_range(
        start=history["ds"].iloc[0],
        periods=len(history) + days,
        freq="D"
    )
    predictions = model.predict(forecast_index)

    residuals = history["y"] - model.predict(history[["time_index"]])
    spread = float(np.std(residuals, ddof=1)) if len(history) > 1 else 0.0

    forecast = pd.DataFrame(
        {
            "ds": forecast_dates,
            "yhat": predictions,
            "yhat_lower": predictions - 1.96 * spread,
            "yhat_upper": predictions + 1.96 * spread,
        }
    )

    return forecast