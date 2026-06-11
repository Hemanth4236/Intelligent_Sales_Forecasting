import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def train_model(df, model_name="Random Forest"):

    numeric_df = df.select_dtypes(include="number")

    if "Sales_Revenue" not in numeric_df.columns:
        raise Exception(
            "Sales_Revenue column not found."
        )

    X = numeric_df.drop(
        columns=["Sales_Revenue"]
    )

    y = numeric_df["Sales_Revenue"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    if model_name == "Linear Regression":
        model = LinearRegression()
    else:
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    joblib.dump(
        model,
        "models/sales_model.pkl"
    )

    results_df = pd.DataFrame(
        {
            "Actual": y_test.values,
            "Predicted": predictions,
        },
        index=y_test.index,
    )

    results_df["Error"] = results_df["Actual"] - results_df["Predicted"]
    results_df["Absolute_Error"] = results_df["Error"].abs()

    feature_importance = None

    if hasattr(model, "feature_importances_"):
        feature_importance = pd.DataFrame(
            {
                "Feature": X.columns,
                "Importance": model.feature_importances_,
            }
        ).sort_values("Importance", ascending=False)
    elif hasattr(model, "coef_"):
        feature_importance = pd.DataFrame(
            {
                "Feature": X.columns,
                "Importance": abs(model.coef_),
            }
        ).sort_values("Importance", ascending=False)

    return model, mae, rmse, r2, results_df, feature_importance