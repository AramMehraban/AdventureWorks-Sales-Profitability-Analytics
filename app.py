
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AdventureWorks | Aram Mehraban",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(85,214,190,.08), transparent 30%),
            linear-gradient(135deg, #0b1220 0%, #111c2d 55%, #0b1220 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101a2a 0%, #0b1220 100%);
        border-right: 1px solid rgba(145,164,184,.18);
    }

    .hero {
        padding: 30px 32px;
        border: 1px solid rgba(85,214,190,.35);
        border-radius: 22px;
        background: linear-gradient(
            115deg, rgba(25,59,67,.72), rgba(21,31,49,.92)
        );
        margin-bottom: 24px;
    }

    .hero-kicker, .section-label {
        color: #55d6be;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: clamp(27px, 3vw, 42px);
        line-height: 1.15;
        font-weight: 800;
        color: #f3f7fb;
        margin: 12px 0;
    }

    .hero-subtitle {
        color: #b7c6d8;
        font-size: 15px;
        line-height: 1.7;
        max-width: 1000px;
    }

    .metric-card {
        min-height: 132px;
        padding: 19px 20px;
        border: 1px solid rgba(145,164,184,.2);
        border-radius: 16px;
        background: linear-gradient(
            145deg, rgba(27,42,62,.94), rgba(17,28,45,.96)
        );
        box-shadow: 0 8px 25px rgba(0,0,0,.12);
        margin-bottom: 12px;
    }

    .metric-label {
        color: #9fb2c8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .8px;
    }

    .metric-value {
        color: #f2f7fb;
        font-size: clamp(22px, 2vw, 31px);
        font-weight: 800;
        margin: 10px 0 7px 0;
        overflow-wrap: anywhere;
    }

    .metric-note {
        color: #91a4b8;
        font-size: 11px;
    }

    .info-card {
        padding: 19px 21px;
        border: 1px solid rgba(145,164,184,.2);
        border-left: 3px solid #55d6be;
        border-radius: 14px;
        background: rgba(22,34,52,.88);
        margin: 12px 0;
    }

    .info-title {
        color: #e8f0f8;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .info-text {
        color: #b7c6d8;
        font-size: 13px;
        line-height: 1.7;
    }

    .footer {
        text-align: center;
        color: #91a4b8;
        border-top: 1px solid rgba(145,164,184,.18);
        margin-top: 36px;
        padding: 24px 8px 8px 8px;
        font-size: 12px;
        line-height: 1.8;
    }

    .stMarkdown h2, .stMarkdown h3 {
        text-align: center;
    }

    div[data-testid="stMetric"] {
        background: rgba(27,42,62,.7);
        border: 1px solid rgba(145,164,184,.18);
        padding: 12px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. COLORS AND CHART SETTINGS
# ============================================================

ACCENT = "#55d6be"
BLUE = "#63a8ff"
PURPLE = "#b59cff"
ORANGE = "#ffbd69"
RED = "#ff7979"

CHART_LAYOUT = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#dce5ee", "family": "Arial"},
    "margin": {"l": 20, "r": 20, "t": 65, "b": 30},
}


# ============================================================
# 4. DATA LOADING AND CLEANING
# ============================================================

@st.cache_data(show_spinner="Loading and preparing sales data...")
def load_data():
    candidates = [
        Path("data/processed/sales_featured.csv"),
        Path("data/processed/sales_clean.csv"),
        Path("data/raw/sales_data.csv"),
    ]

    data_path = next((path for path in candidates if path.exists()), None)

    if data_path is None:
        return None, None

    data = pd.read_csv(data_path, low_memory=False)

    # Remove accidental CSV index columns.
    data = data.loc[
        :, ~data.columns.astype(str).str.match(r"^Unnamed:")
    ].copy()

    aliases = {
        "OrderDate": ["OrderDate", "order_date", "Order Date"],
        "SalesAmount": ["SalesAmount", "sales_amount", "Sales Amount"],
        "TotalProductCost": [
            "TotalProductCost",
            "total_product_cost",
            "Total Product Cost",
        ],
        "Profit": ["Profit", "profit"],
        "SalesOrderNumber": [
            "SalesOrderNumber",
            "sales_order_number",
            "Sales Order Number",
        ],
        "CustomerKey": ["CustomerKey", "customer_key", "Customer Key"],
        "Country": [
            "Country",
            "country",
            "EnglishCountryRegionName",
        ],
        "ProductCategoryName": [
            "ProductCategoryName",
            "product_category_name",
            "Product Category",
            "Category",
        ],
        "ProductName": [
            "ProductName",
            "product_name",
            "Product Name",
        ],
    }

    for standard_name, possible_names in aliases.items():
        if standard_name not in data.columns:
            match = next(
                (
                    name for name in possible_names
                    if name in data.columns
                ),
                None,
            )
            if match:
                data.rename(
                    columns={match: standard_name},
                    inplace=True,
                )

    required_columns = [
        "OrderDate",
        "SalesAmount",
        "Profit",
        "SalesOrderNumber",
        "Country",
        "ProductCategoryName",
        "ProductName",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        return {
            "missing_columns": missing_columns,
            "available_columns": list(data.columns),
        }, data_path.as_posix()

    data["OrderDate"] = pd.to_datetime(
        data["OrderDate"], errors="coerce"
    )

    numeric_columns = [
        "SalesAmount",
        "TotalProductCost",
        "Profit",
        "CustomerKey",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )

    # Calculate cost only if the source does not provide it.
    if "TotalProductCost" not in data.columns:
        data["TotalProductCost"] = (
            data["SalesAmount"] - data["Profit"]
        )

    data = data.dropna(
        subset=["OrderDate", "SalesAmount", "Profit"]
    ).copy()

    for column in [
        "Country",
        "ProductCategoryName",
        "ProductName",
    ]:
        data[column] = (
            data[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .replace("", "Unknown")
        )

    data["SalesOrderNumber"] = (
        data["SalesOrderNumber"]
        .fillna("Unknown")
        .astype(str)
    )

    data["YearMonth"] = data["OrderDate"].dt.to_period("M").astype(str)
    data["Year"] = data["OrderDate"].dt.year
    data["Month"] = data["OrderDate"].dt.month

    data["ProfitMargin"] = np.where(
        data["SalesAmount"] != 0,
        data["Profit"] / data["SalesAmount"] * 100,
        np.nan,
    )

    return data, data_path.as_posix()


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def number(value, decimals=0):
    if pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}"


def percent(value, decimals=1):
    if pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}%"


def unique_count(series):
    return int(series.nunique()) if series is not None else 0


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=360):
    fig.update_layout(**CHART_LAYOUT, height=height)
    return fig


def show_empty(message):
    st.info(message)


def aggregate_sales(data, group_column):
    result = (
        data.groupby(group_column, dropna=False)
        .agg(
            Sales=("SalesAmount", "sum"),
            Profit=("Profit", "sum"),
            Cost=("TotalProductCost", "sum"),
            Orders=("SalesOrderNumber", "nunique"),
        )
        .reset_index()
    )

    result["Margin"] = np.where(
        result["Sales"] != 0,
        result["Profit"] / result["Sales"] * 100,
        np.nan,
    )

    return result


def set_checkbox_group(keys, value):
    for key in keys:
        st.session_state[key] = value


def reset_dashboard_filters(
    min_date, max_date, country_keys, category_keys
):
    st.session_state["order_date_range"] = (min_date, max_date)

    for key in country_keys + category_keys:
        st.session_state[key] = True


# ============================================================
# 6. HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">
            BUSINESS INTELLIGENCE · DATA ANALYTICS PORTFOLIO
        </div>
        <div class="hero-title">
            AdventureWorks Sales &amp; Profitability Analytics
        </div>
        <div class="hero-subtitle">
            An end-to-end analytics project covering sales performance,
            product profitability, customer activity, market comparisons
            and business recommendations.<br><br>
            <b>Created by Aram Mehraban</b>
            &nbsp; · &nbsp; SQL Server · Python · Excel · Power BI · Streamlit
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 7. LOAD DATA
# ============================================================

df, source_path = load_data()

if df is None:
    st.error("Dataset not found. Expected one of these files:")
    st.code(
        "data/processed/sales_featured.csv\n"
        "data/processed/sales_clean.csv\n"
        "data/raw/sales_data.csv"
    )
    st.info(
        "Run Streamlit from your project root folder, "
        "or update the file paths in load_data()."
    )
    st.stop()

if isinstance(df, dict) and "missing_columns" in df:
    st.error("Required columns are missing from the dataset.")
    st.write("Missing columns:", df["missing_columns"])
    st.write("Available columns:", df["available_columns"])
    st.stop()

if df.empty:
    st.warning("The dataset contains no usable records.")
    st.stop()


# ============================================================
# 8. SIDEBAR AND FILTERS
# ============================================================

st.sidebar.markdown(
    """
    <div style="padding:12px 0 18px 0;">
        <div style="
            width:54px;height:54px;border-radius:15px;
            background:#193b43;border:1px solid #55d6be;
            display:flex;align-items:center;justify-content:center;
            color:#55d6be;font-size:22px;font-weight:800;">
            AM
        </div>
        <div style="font-size:19px;font-weight:750;margin-top:12px;">
            Aram Mehraban
        </div>
        <div style="font-size:12px;color:#91a4b8;">
            Data Analytics Portfolio
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## Dashboard Filters")
st.sidebar.caption("All KPIs and charts respond to your selections.")

min_date = df["OrderDate"].min().date()
max_date = df["OrderDate"].max().date()

if "order_date_range" not in st.session_state:
    st.session_state["order_date_range"] = (min_date, max_date)

selected_dates = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="order_date_range",
)

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
    start_date = end_date = selected_dates[0]
else:
    start_date, end_date = min_date, max_date

country_options = sorted(df["Country"].unique().tolist())
category_options = sorted(
    df["ProductCategoryName"].unique().tolist()
)

country_keys = [
    f"country_filter_{i}" for i in range(len(country_options))
]
category_keys = [
    f"category_filter_{i}" for i in range(len(category_options))
]

for key in country_keys + category_keys:
    if key not in st.session_state:
        st.session_state[key] = True

with st.sidebar.expander("Country / Market", expanded=True):
    selected_count = sum(
        bool(st.session_state[key]) for key in country_keys
    )
    st.caption(
        f"{selected_count} of {len(country_options)} markets selected"
    )

    select_col, clear_col = st.columns(2)

    select_col.button(
        "Select all",
        key="select_all_countries",
        use_container_width=True,
        on_click=set_checkbox_group,
        args=(country_keys, True),
    )

    clear_col.button(
        "Clear all",
        key="clear_all_countries",
        use_container_width=True,
        on_click=set_checkbox_group,
        args=(country_keys, False),
    )

    for country, key in zip(country_options, country_keys):
        st.checkbox(country, key=key)

selected_countries = [
    country for country, key in zip(country_options, country_keys)
    if st.session_state[key]
]

with st.sidebar.expander("Product Category", expanded=True):
    selected_count = sum(
        bool(st.session_state[key]) for key in category_keys
    )
    st.caption(
        f"{selected_count} of {len(category_options)} categories selected"
    )

    select_col, clear_col = st.columns(2)

    select_col.button(
        "Select all",
        key="select_all_categories",
        use_container_width=True,
        on_click=set_checkbox_group,
        args=(category_keys, True),
    )

    clear_col.button(
        "Clear all",
        key="clear_all_categories",
        use_container_width=True,
        on_click=set_checkbox_group,
        args=(category_keys, False),
    )

    for category, key in zip(category_options, category_keys):
        st.checkbox(category, key=key)

selected_categories = [
    category for category, key in zip(category_options, category_keys)
    if st.session_state[key]
]

filtered = df[
    (df["OrderDate"] >= pd.Timestamp(start_date))
    & (
        df["OrderDate"]
        < pd.Timestamp(end_date) + pd.Timedelta(days=1)
    )
    & df["Country"].isin(selected_countries)
    & df["ProductCategoryName"].isin(selected_categories)
].copy()

st.sidebar.divider()

st.sidebar.markdown("### About this project")
st.sidebar.caption(
    "Interactive portfolio demonstration using AdventureWorks sales data."
)

st.sidebar.button(
    "Reset filters",
    key="reset_dashboard_filters_button",
    use_container_width=True,
    on_click=reset_dashboard_filters,
    args=(min_date, max_date, country_keys, category_keys),
)


# ============================================================
# 9. FILTER VALIDATION
# ============================================================

if filtered.empty:
    st.warning(
        "No records match the selected filters. "
        "Select a wider date range or add markets/categories."
    )
    st.stop()


# ============================================================
# 10. KPI CALCULATIONS
# ============================================================

total_sales = filtered["SalesAmount"].sum()
total_profit = filtered["Profit"].sum()
total_cost = filtered["TotalProductCost"].sum()

total_orders = unique_count(filtered["SalesOrderNumber"])

if "CustomerKey" in filtered.columns:
    total_customers = unique_count(filtered["CustomerKey"])
else:
    total_customers = 0

total_products = unique_count(filtered["ProductName"])

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else np.nan
)

average_order_value = (
    total_sales / total_orders
    if total_orders > 0 else np.nan
)


# ============================================================
# 11. TOP-LEVEL KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-label">Executive Overview</div>',
    unsafe_allow_html=True,
)

st.subheader("Sales performance at a glance")

kpi_columns = st.columns(4)

with kpi_columns[0]:
    metric_card("Total Sales", number(total_sales), "Sum of sales amount")

with kpi_columns[1]:
    metric_card("Total Profit", number(total_profit), "Sum of recorded profit")

with kpi_columns[2]:
    metric_card("Profit Margin", percent(profit_margin, 2), "Profit ÷ Sales")

with kpi_columns[3]:
    metric_card("Total Orders", number(total_orders), "Distinct order numbers")

kpi_columns_2 = st.columns(4)

with kpi_columns_2[0]:
    metric_card("Customers", number(total_customers), "Distinct customer keys")

with kpi_columns_2[1]:
    metric_card("Products", number(total_products), "Distinct product names")

with kpi_columns_2[2]:
    metric_card(
        "Average Order Value",
        number(average_order_value, 2),
        "Sales ÷ distinct orders",
    )

with kpi_columns_2[3]:
    metric_card("Total Cost", number(total_cost), "Sum of product cost")

st.caption(
    f"Showing {len(filtered):,} records from "
    f"{start_date.strftime('%d %b %Y')} to "
    f"{end_date.strftime('%d %b %Y')}."
)


# ============================================================
# 12. DASHBOARD TABS
# ============================================================

(
    tab_overview,
    tab_markets,
    tab_products,
    tab_insights,
    tab_method,
) = st.tabs(
    [
        "Executive Overview",
        "Sales & Markets",
        "Products & Profit",
        "Insights & Actions",
        "Data & Methodology",
    ]
)


# ============================================================
# TAB 1: EXECUTIVE OVERVIEW
# ============================================================

with tab_overview:
    st.markdown("### Sales trend and business performance")

    monthly = (
        filtered.groupby("YearMonth", as_index=False)
        .agg(
            Sales=("SalesAmount", "sum"),
            Profit=("Profit", "sum"),
        )
        .sort_values("YearMonth")
    )

    category_summary = aggregate_sales(
        filtered, "ProductCategoryName"
    ).sort_values("Sales", ascending=False)

    left, right = st.columns([1.7, 1])

    with left:
        if not monthly.empty:
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=monthly["YearMonth"],
                    y=monthly["Sales"],
                    name="Sales",
                    mode="lines+markers",
                    line={"color": ACCENT, "width": 3},
                    fill="tozeroy",
                    fillcolor="rgba(85,214,190,0.08)",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=monthly["YearMonth"],
                    y=monthly["Profit"],
                    name="Profit",
                    mode="lines+markers",
                    line={"color": BLUE, "width": 2},
                )
            )

            fig.update_layout(
                title={
                    "text": "Monthly Sales & Profit",
                    "x": 0.5,
                    "xanchor": "center",
                },
                xaxis_title="Month",
                yaxis_title="Amount",
                hovermode="x unified",
            )

            st.plotly_chart(
                style_chart(fig, 390),
                use_container_width=True,
            )
        else:
            show_empty("Not enough date information to display the trend.")

    with right:
        if not category_summary.empty:
            fig = px.pie(
                category_summary,
                names="ProductCategoryName",
                values="Sales",
                hole=0.60,
                title="Sales Mix by Category",
                color_discrete_sequence=[
                    ACCENT, BLUE, PURPLE, ORANGE, RED
                ],
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate=(
                    "%{label}<br>Sales: %{value:,.0f}"
                    "<br>Share: %{percent}<extra></extra>"
                ),
            )

            fig.update_layout(
                title={
                    "text": "Sales Mix by Category",
                    "x": 0.5,
                    "xanchor": "center",
                }
            )

            st.plotly_chart(
                style_chart(fig, 390),
                use_container_width=True,
            )
        else:
            show_empty("No category data is available for this selection.")

    st.markdown("### Performance by product category")

    if not category_summary.empty:
        fig = px.bar(
            category_summary.sort_values("Sales"),
            x="Sales",
            y="ProductCategoryName",
            orientation="h",
            color="Profit",
            color_continuous_scale="Teal",
            title="Sales by Category, Colored by Profit",
            hover_data={
                "Sales": ":,.0f",
                "Profit": ":,.0f",
                "Margin": ":.2f",
            },
        )

        fig.update_layout(
            xaxis_title="Sales",
            yaxis_title="",
            coloraxis_colorbar_title="Profit",
        )

        st.plotly_chart(
            style_chart(fig, 350),
            use_container_width=True,
        )

    st.markdown("### Selected-period summary")

    summary_data = pd.DataFrame(
        {
            "Metric": [
                "Sales",
                "Profit",
                "Margin",
                "Orders",
                "Customers",
                "Average Order Value",
            ],
            "Value": [
                number(total_sales),
                number(total_profit),
                percent(profit_margin, 2),
                number(total_orders),
                number(total_customers),
                number(average_order_value, 2),
            ],
        }
    )

    st.dataframe(
        summary_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TAB 2: SALES & MARKETS
# ============================================================

with tab_markets:
    st.markdown("### Geographic sales performance")

    country_summary = aggregate_sales(
        filtered, "Country"
    ).sort_values("Sales", ascending=False)

    if country_summary.empty:
        show_empty("No market data available for these filters.")
    else:
        total_market_sales = country_summary["Sales"].sum()

        country_summary["SalesShare"] = np.where(
            total_market_sales != 0,
            country_summary["Sales"] / total_market_sales * 100,
            0,
        )

        left, right = st.columns(2)

        with left:
            fig = px.bar(
                country_summary.sort_values("Sales"),
                x="Sales",
                y="Country",
                orientation="h",
                title="Sales by Country",
                color="Sales",
                color_continuous_scale="Teal",
                hover_data={
                    "Profit": ":,.0f",
                    "Margin": ":.2f",
                    "SalesShare": ":.2f",
                },
            )

            fig.update_layout(
                xaxis_title="Sales",
                yaxis_title="",
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                style_chart(fig, 400),
                use_container_width=True,
            )

        with right:
            fig = px.bar(
                country_summary.sort_values("Margin"),
                x="Margin",
                y="Country",
                orientation="h",
                title="Profit Margin by Country",
                color="Margin",
                color_continuous_scale="Teal",
                hover_data={
                    "Sales": ":,.0f",
                    "Profit": ":,.0f",
                },
            )

            fig.update_layout(
                xaxis_title="Profit margin (%)",
                yaxis_title="",
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                style_chart(fig, 400),
                use_container_width=True,
            )

    st.markdown("### Market Comparison")

    if country_summary.empty:
        show_empty("No market data is available for the selected filters.")
    else:
        market_table = country_summary[
            ["Country", "Sales", "Profit", "Orders", "Margin"]
        ].copy()

        market_table = market_table.rename(
            columns={
                "Country": "Market",
                "Margin": "Margin (%)",
            }
        )

        st.dataframe(
            market_table.style.format(
                {
                    "Sales": "{:,.0f}",
                    "Profit": "{:,.0f}",
                    "Orders": "{:,.0f}",
                    "Margin (%)": "{:.2f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download market analysis as CSV",
            data=market_table.to_csv(index=False).encode("utf-8-sig"),
            file_name="adventureworks_market_analysis.csv",
            mime="text/csv",
        )


# ============================================================
# TAB 3: PRODUCTS & PROFIT
# ============================================================

with tab_products:
    st.markdown("### Product performance and profitability")

    product_summary = (
        filtered.groupby(
            ["ProductName", "ProductCategoryName"],
            dropna=False,
        )
        .agg(
            Sales=("SalesAmount", "sum"),
            Profit=("Profit", "sum"),
            Cost=("TotalProductCost", "sum"),
            Orders=("SalesOrderNumber", "nunique"),
        )
        .reset_index()
    )

    product_summary["Margin"] = np.where(
        product_summary["Sales"] != 0,
        product_summary["Profit"] / product_summary["Sales"] * 100,
        np.nan,
    )

    top_n = st.slider(
        "Number of products to display",
        min_value=5,
        max_value=20,
        value=10,
        step=5,
        key="top_products_n",
    )

    top_products = product_summary.nlargest(top_n, "Sales")

    left, right = st.columns(2)

    with left:
        if not top_products.empty:
            fig = px.bar(
                top_products.sort_values("Sales"),
                x="Sales",
                y="ProductName",
                orientation="h",
                title=f"Top {top_n} Products by Sales",
                color="Sales",
                color_continuous_scale="Teal",
                hover_data={
                    "Profit": ":,.0f",
                    "Margin": ":.2f",
                    "ProductCategoryName": True,
                },
            )

            fig.update_layout(
                xaxis_title="Sales",
                yaxis_title="",
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                style_chart(fig, 470),
                use_container_width=True,
            )

    with right:
        if not top_products.empty:
            fig = px.bar(
                top_products.sort_values("Profit"),
                x="Profit",
                y="ProductName",
                orientation="h",
                title=f"Profit from Top {top_n} Sales Products",
                color="Profit",
                color_continuous_scale="Teal",
                hover_data={
                    "Sales": ":,.0f",
                    "Margin": ":.2f",
                },
            )

            fig.update_layout(
                xaxis_title="Profit",
                yaxis_title="",
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                style_chart(fig, 470),
                use_container_width=True,
            )

    st.markdown("### Category profitability")

    category_profit = aggregate_sales(
        filtered, "ProductCategoryName"
    ).sort_values("Margin", ascending=False)

    if not category_profit.empty:
        fig = px.bar(
            category_profit,
            x="ProductCategoryName",
            y="Margin",
            title="Profit Margin by Product Category",
            color="Margin",
            color_continuous_scale="Teal",
            hover_data={
                "Sales": ":,.0f",
                "Profit": ":,.0f",
                "Cost": ":,.0f",
            },
        )

        fig.update_layout(
            xaxis_title="Product category",
            yaxis_title="Profit margin (%)",
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            style_chart(fig, 360),
            use_container_width=True,
        )

    st.markdown("### Product Details")

    product_table = (
        product_summary.sort_values("Sales", ascending=False)
        .head(top_n)[
            [
                "ProductName",
                "ProductCategoryName",
                "Sales",
                "Profit",
                "Orders",
                "Margin",
            ]
        ]
        .rename(
            columns={
                "ProductName": "Product",
                "ProductCategoryName": "Category",
                "Margin": "Margin (%)",
            }
        )
    )

    st.dataframe(
        product_table.style.format(
            {
                "Sales": "{:,.0f}",
                "Profit": "{:,.0f}",
                "Orders": "{:,.0f}",
                "Margin (%)": "{:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download product analysis as CSV",
        data=product_table.to_csv(index=False).encode("utf-8-sig"),
        file_name="adventureworks_product_analysis.csv",
        mime="text/csv",
    )


# ============================================================
# TAB 4: INSIGHTS & ACTIONS
# ============================================================

with tab_insights:
    st.markdown("### Business insights and recommended next steps")

    category_insights = aggregate_sales(
        filtered, "ProductCategoryName"
    )

    country_insights = aggregate_sales(filtered, "Country")

    product_insights = (
        filtered.groupby("ProductName", dropna=False)
        .agg(
            Sales=("SalesAmount", "sum"),
            Profit=("Profit", "sum"),
        )
        .reset_index()
    )

    if not category_insights.empty:
        highest_sales_category = category_insights.loc[
            category_insights["Sales"].idxmax()
        ]

        highest_margin_category = category_insights.loc[
            category_insights["Margin"].idxmax()
        ]

        lowest_margin_category = category_insights.loc[
            category_insights["Margin"].idxmin()
        ]

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">01 · Revenue concentration</div>
                <div class="info-text">
                    <b>{highest_sales_category['ProductCategoryName']}</b>
                    is the largest sales category in the current selection,
                    generating <b>{number(highest_sales_category['Sales'])}</b>
                    in sales.
                    <br><br>
                    <b>Recommended action:</b> monitor its sales trend,
                    inventory availability and profit contribution.
                    High sales volume does not automatically mean the
                    highest margin.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">02 · Profitability opportunities</div>
                <div class="info-text">
                    <b>{highest_margin_category['ProductCategoryName']}</b>
                    has the highest category margin at
                    <b>{percent(highest_margin_category['Margin'], 2)}</b>.
                    The lowest margin is recorded for
                    <b>{lowest_margin_category['ProductCategoryName']}</b>
                    at <b>{percent(lowest_margin_category['Margin'], 2)}</b>.
                    <br><br>
                    <b>Recommended action:</b> compare cost structure,
                    discounts, product mix and pricing before changing
                    prices or product strategy.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not country_insights.empty:
        leading_country = country_insights.loc[
            country_insights["Sales"].idxmax()
        ]

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">03 · Market performance</div>
                <div class="info-text">
                    <b>{leading_country['Country']}</b> leads selected
                    markets with <b>{number(leading_country['Sales'])}</b>
                    in sales and a profit margin of
                    <b>{percent(leading_country['Margin'], 2)}</b>.
                    <br><br>
                    <b>Recommended action:</b> compare product mix and
                    margin with other markets to understand the effects
                    of sales volume, cost and category mix.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not product_insights.empty:
        leading_product = product_insights.loc[
            product_insights["Sales"].idxmax()
        ]

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">04 · Product performance</div>
                <div class="info-text">
                    <b>{leading_product['ProductName']}</b> is the top
                    product by sales in the current selection, with
                    <b>{number(leading_product['Sales'])}</b> in sales
                    and <b>{number(leading_product['Profit'])}</b> in profit.
                    <br><br>
                    <b>Recommended action:</b> review margin, sales
                    consistency and revenue contribution before making
                    inventory decisions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-title">05 · Data-driven decision-making</div>
            <div class="info-text">
                The current selection contains <b>{number(len(filtered))}</b>
                sales records, <b>{number(total_orders)}</b> distinct orders
                and <b>{number(total_customers)}</b> distinct customers.
                <br><br>
                <b>Recommended action:</b> use the filters to test whether
                findings remain consistent across different periods,
                markets and product categories.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "These are descriptive analytics findings based on the selected data. "
        "Validate them with business context before operational decisions."
    )


# ============================================================
# TAB 5: DATA & METHODOLOGY
# ============================================================

with tab_method:
    st.markdown("### Project overview")

    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">Project objective</div>
            <div class="info-text">
                Build an end-to-end Business Intelligence workflow to
                evaluate sales performance, profitability, customer
                activity, product categories and geographic markets.
                The project demonstrates data extraction, validation,
                analytical preparation, KPI calculation and interactive
                reporting.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Technical workflow")

    workflow_columns = st.columns(5)

    workflow_items = [
        ("01", "SQL Server", "Extract sales and dimension data"),
        ("02", "Python", "Clean, validate and transform data"),
        ("03", "Excel", "Support data review and reporting"),
        ("04", "Power BI", "Build the interactive BI report"),
        ("05", "Streamlit", "Publish a web-based portfolio demo"),
    ]

    for column, item in zip(workflow_columns, workflow_items):
        number_label, title_label, description = item

        with column:
            st.markdown(
                f"""
                <div class="info-card" style="min-height:155px;">
                    <div class="section-label">{number_label}</div>
                    <div class="info-title">{title_label}</div>
                    <div class="info-text">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### Data quality checks")

    quality_results = [
        ("Missing order dates", int(df["OrderDate"].isna().sum())),
        ("Missing sales values", int(df["SalesAmount"].isna().sum())),
        ("Missing profit values", int(df["Profit"].isna().sum())),
        ("Negative sales records", int((df["SalesAmount"] < 0).sum())),
        ("Negative cost records", int((df["TotalProductCost"] < 0).sum())),
        ("Duplicate rows", int(df.duplicated().sum())),
    ]

    st.dataframe(
        pd.DataFrame(
            quality_results,
            columns=["Check", "Records"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "These checks are calculated on the loaded dataset after basic "
        "type and date/value cleaning. They do not replace a complete "
        "validation of the source database."
    )

    st.markdown("### Current dataset")

    dataset_info = pd.DataFrame(
        [
            ("Loaded file", source_path),
            ("Rows after validation", number(len(df))),
            ("Columns", number(len(df.columns))),
            ("First order date", str(df["OrderDate"].min().date())),
            ("Last order date", str(df["OrderDate"].max().date())),
            ("Distinct countries", number(unique_count(df["Country"]))),
            (
                "Distinct categories",
                number(unique_count(df["ProductCategoryName"])),
            ),
            ("Distinct products", number(unique_count(df["ProductName"]))),
        ],
        columns=["Property", "Value"],
    )

    st.dataframe(
        dataset_info,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Technologies")

    st.write(
        "SQL Server · Python · Pandas · NumPy · Plotly · "
        "Streamlit · Excel · Power BI"
    )

    st.markdown("### Project author")

    st.markdown(
        """
        **Aram Mehraban**

        Data Analyst | BI & Reporting | SQL | Power BI | Python | GIS

        Portfolio project developed to demonstrate practical data analysis,
        data quality validation, KPI design and business reporting.
        """
    )

    st.info(
        "Sales amounts are displayed in the source dataset's numeric units. "
        "No currency symbol is added because the currency has not been "
        "confirmed in this application."
    )


# ============================================================
# 13. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <b>ADVENTUREWORKS SALES &amp; PROFITABILITY ANALYTICS</b><br>
        Portfolio demonstration by Aram Mehraban ·
        SQL Server · Python · Power BI · Streamlit
        <br><br>
        Interactive analysis for portfolio and demonstration purposes.
        Findings should be interpreted in the context of the underlying dataset.
    </div>
    """,
    unsafe_allow_html=True,
)
