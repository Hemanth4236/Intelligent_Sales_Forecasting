import pandas as pd

def preprocess_data(df):

    df = df.copy()

    df = df.drop_duplicates()

    df = df.dropna()

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        df["DayOfWeek"] = df["Date"].dt.day_name()

    if {"Sales_Revenue", "Inventory_Level"}.issubset(df.columns):
        df["Revenue_to_Inventory"] = df["Sales_Revenue"] / df["Inventory_Level"].replace(0, pd.NA)

    if {"Quantity_Sold", "Reorder_Point"}.issubset(df.columns):
        df["Reorder_Gap"] = df["Reorder_Point"] - df["Quantity_Sold"]

    sort_columns = [column for column in ["Date", "Product_Name"] if column in df.columns]

    if sort_columns:
        df = df.sort_values(by=sort_columns, ascending=[False] * len(sort_columns))

    if "Date" in df.columns:
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    return df