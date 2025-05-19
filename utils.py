import pandas as pd
import plotly.express as px

def load_data():
    return pd.read_csv("data/sample_sales_data.csv")

def save_data(df):
    df.to_csv("data/updated_sales_data.csv", index=False)

def generate_kpis(df):
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales else 0
    return total_sales, total_profit, profit_margin

def plot_sales_by_region(df):
    fig = px.bar(df.groupby("Region")["Sales"].sum().reset_index(), x='Region', y='Sales', title='Sales by Region')
    return fig

def plot_customer_ages(df):
    return px.histogram(df, x='Customer Age', nbins=20, title='Customer Age Distribution')

def plot_gender_split(df):
    return px.pie(df, names='Customer Gender', title='Customer Gender Distribution')
