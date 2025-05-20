import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF


def load_data():
    return pd.read_csv("data/sample_sales_data.csv")


def generate_kpis(df):
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0
    return total_sales, total_profit, profit_margin


def plot_sales_by_region(df):
    summary = df.groupby("Region")["Sales"].sum().reset_index()
    fig = px.bar(
        summary, x="Region", y="Sales", color="Region",
        title="Sales by Region", text_auto=True
    )
    fig.update_traces(hovertemplate="Region: %{x}<br>Sales: $%{y:,.2f}")
    return fig


def plot_customer_ages(df):
    fig = px.histogram(
        df, x="Customer Age", nbins=20, color="Customer Gender",
        title="Customer Age Distribution", marginal="rug"
    )
    fig.update_traces(hovertemplate="Age: %{x}<br>Count: %{y}")
    return fig


def plot_gender_split(df):
    fig = px.pie(
        df, names="Customer Gender", title="Customer Gender Split",
        color="Customer Gender", hole=0.4
    )
    fig.update_traces(hovertemplate="%{label}: %{percent}")
    return fig


def export_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales Data')
    output.seek(0)
    return output


def export_to_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    col_width = pdf.w / (len(df.columns) + 1)

    # Header
    for col in df.columns:
        pdf.cell(col_width, 10, str(col), border=1)
    pdf.ln()

    # Rows
    for i, row in df.iterrows():
        for item in row:
            cell_text = str(item)
            if len(cell_text) > 15:
                cell_text = cell_text[:12] + "..."
            pdf.cell(col_width, 10, cell_text, border=1)
        pdf.ln()
        if i > 20: break  # Prevent overflow

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
