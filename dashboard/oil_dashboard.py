# ============================================================
# Oil Price Dashboard
# Part 1
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart
)


def show_oil_dashboard(master):

    st.title("🛢 Oil Price Analysis Dashboard")

    st.markdown("""
    Analyze historical oil prices and their trends over time.
    """)

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    avg_price = master["Average_Oil_Price"].mean()

    highest_price = master["Average_Oil_Price"].max()

    lowest_price = master["Average_Oil_Price"].min()

    latest_year = master["Year"].max()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "🛢 Avg Oil Price",
        f"${avg_price:.2f}"
    )

    c2.metric(
        "📈 Highest Price",
        f"${highest_price:.2f}"
    )

    c3.metric(
        "📉 Lowest Price",
        f"${lowest_price:.2f}"
    )

    c4.metric(
        "📅 Latest Year",
        latest_year
    )

    st.divider()

    # ============================================================
    # Oil Trend
    # ============================================================

    oil = (

        master

        .groupby("Year")["Average_Oil_Price"]

        .mean()

        .reset_index()

    )

    st.subheader("📈 Global Oil Price Trend")

    st.plotly_chart(

        line_chart(

            oil,

            "Year",

            "Average_Oil_Price",

            "Average Oil Price",

            "#1E90FF"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Highest Oil Price Years
    # ============================================================

    st.subheader("🔥 Highest Oil Price Years")

    highest = (

        oil

        .sort_values(

            "Average_Oil_Price",

            ascending=False

        )

        .head(10)

    )

    st.plotly_chart(

        bar_chart(

            highest,

            "Year",

            "Average_Oil_Price",

            "Highest Oil Price Years"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Lowest Oil Price Years
    # ============================================================

    st.subheader("❄ Lowest Oil Price Years")

    lowest = (

        oil

        .sort_values(

            "Average_Oil_Price"

        )

        .head(10)

    )

    st.plotly_chart(

        bar_chart(

            lowest,

            "Year",

            "Average_Oil_Price",

            "Lowest Oil Price Years"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Summary Table
    # ============================================================

    st.subheader("📅 Oil Price Summary")

    st.dataframe(

        oil,

        use_container_width=True,

        hide_index=True

    )


    # ============================================================
    # Oil Price Distribution
    # ============================================================

    st.subheader("📊 Oil Price Distribution")

    st.bar_chart(
        master["Average_Oil_Price"].dropna().value_counts(bins=20)
    )

    st.divider()

    # ============================================================
    # Year-over-Year Oil Price Change
    # ============================================================

    st.subheader("📈 Year-over-Year Oil Price Change")

    oil_change = oil.copy()

    oil_change["Oil_Price_Change"] = (
        oil_change["Average_Oil_Price"].diff()
    )

    import plotly.express as px

    fig = px.bar(

        oil_change,

        x="Year",

        y="Oil_Price_Change",

        title="Yearly Oil Price Change",

        color="Oil_Price_Change",

        color_continuous_scale="RdYlGn"

    )

    fig.update_layout(

        template="plotly_dark",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Rolling Average
    # ============================================================

    st.subheader("📉 3-Year Rolling Average")

    oil_change["Rolling_Average"] = (

        oil_change["Average_Oil_Price"]

        .rolling(3)

        .mean()

    )

    fig = px.line(

        oil_change,

        x="Year",

        y=[

            "Average_Oil_Price",

            "Rolling_Average"

        ],

        markers=True,

        title="Oil Price vs Rolling Average"

    )

    fig.update_layout(

        template="plotly_dark",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Oil Price Volatility
    # ============================================================

    st.subheader("🌍 Oil Price Volatility")

    oil_change["Volatility"] = (

        oil_change["Average_Oil_Price"]

        .pct_change()

        *100

    )

    fig = px.line(

        oil_change,

        x="Year",

        y="Volatility",

        markers=True,

        title="Oil Price Volatility (%)"

    )

    fig.update_layout(

        template="plotly_dark",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Highest Increase & Biggest Drop
    # ============================================================

    st.subheader("📌 Largest Oil Price Movements")

    c1, c2 = st.columns(2)

    increase = oil_change.loc[
        oil_change["Oil_Price_Change"].idxmax()
    ]

    decrease = oil_change.loc[
        oil_change["Oil_Price_Change"].idxmin()
    ]

    with c1:

        st.success(f"""

### Highest Increase

Year : **{int(increase['Year'])}**

Increase : **{increase['Oil_Price_Change']:.2f}**

""")

    with c2:

        st.error(f"""

### Largest Drop

Year : **{int(decrease['Year'])}**

Decrease : **{decrease['Oil_Price_Change']:.2f}**

""")

    st.divider()

    # ============================================================
    # Business Insights
    # ============================================================

    st.subheader("📌 Oil Market Insights")

    st.success(f"""

### Key Findings

• Years Covered : **{master['Year'].min()} - {master['Year'].max()}**

• Average Oil Price :

**${avg_price:.2f}**

• Highest Oil Price :

**${highest_price:.2f}**

• Lowest Oil Price :

**${lowest_price:.2f}**

• Latest Year Available :

**{latest_year}**

""")

    st.divider()

    # ============================================================
    # Download Dataset
    # ============================================================

    st.download_button(

        "📥 Download Oil Dataset",

        data=master.to_csv(index=False),

        file_name="oil_dashboard.csv",

        mime="text/csv"

    )
