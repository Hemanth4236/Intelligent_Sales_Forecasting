import plotly.express as px

def sales_trend(df):

    fig = px.line(
        df,
        x='Date',
        y='Sales_Revenue',
        title='Sales Trend'
    )

    return fig


def category_sales(df):

    fig = px.bar(
        df,
        x='Category',
        y='Sales_Revenue',
        color='Category',
        title='Category Wise Sales'
    )

    return fig


def region_sales(df):

    fig = px.pie(
        df,
        names='Region',
        values='Sales_Revenue',
        title='Region Wise Sales'
    )

    return fig