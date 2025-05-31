import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF


def load_data():
    """Load sales data from CSV file."""
    return pd.read_csv("data/sample_sales_data.csv")


def generate_kpis(df):
    """Calculate key performance indicators from the sales data."""
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0
    return total_sales, total_profit, profit_margin


def plot_sales_by_region(df):
    """Generate a bar chart of sales by region."""
    summary = df.groupby("Region")["Sales"].sum().reset_index()
    fig = px.bar(
        summary, x="Region", y="Sales", color="Region",
        title="Sales by Region", text_auto=True
    )
    fig.update_traces(hovertemplate="Region: %{x}<br>Sales: $%{y:,.2f}")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig


def plot_customer_ages(df):
    """Create a histogram showing distribution of customer ages."""
    fig = px.histogram(
        df, x="Customer Age", nbins=20, color="Customer Gender",
        title="Customer Age Distribution", marginal="rug"
    )
    fig.update_traces(hovertemplate="Age: %{x}<br>Count: %{y}")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig


def plot_gender_split(df):
    """Display a pie chart showing gender distribution of customers."""
    fig = px.pie(
        df, names="Customer Gender", title="Customer Gender Split",
        color="Customer Gender", hole=0.4
    )
    fig.update_traces(hovertemplate="%{label}: %{percent}")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig


def export_to_excel(df):
    """Export the DataFrame to an in-memory Excel file."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales Data')
    output.seek(0)
    return output


def export_to_pdf(df):
    """
    Export the DataFrame to a PDF file stored in memory (BytesIO).
    Handles column overflow and long text wrapping.
    """
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
            text = str(item)
            if len(text) > 15:
                text = text[:12] + "..."
            pdf.cell(col_width, 10, text, border=1)
        pdf.ln()
        if i >= 25:  # Safety cutoff to prevent page overflow
            pdf.cell(0, 10, "Table truncated for preview...", ln=True)
            break

    # Convert to PDF bytes and return as buffer
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer
