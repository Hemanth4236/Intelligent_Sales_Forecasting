import pandas as pd


def inventory_analysis(df):

    inventory_status = []

    for _, row in df.iterrows():

        stock = row["Inventory_Level"]
        reorder = row["Reorder_Point"]

        if stock < reorder:

            status = "Reorder Required"

        elif stock > reorder * 3:

            status = "Overstock"

        else:

            status = "Healthy"

        inventory_status.append(status)

    df["Inventory_Status"] = inventory_status

    return df