# ============================================================
# Oil Price Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart,
    horizontal_bar_chart,
    histogram_chart
)


def show_oil_dashboard(master):

    st.title("🛢 Oil Price Analysis Dashboard")

    st.markdown("""
Analyze global oil price trends and their changes over time.
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
    # Oil Price Trend
    # ============================================================

    yearly = (

        master

        .groupby("Year")["Average_Oil_Price"]

        .mean()

        .reset_index()

    )

    st.subheader("📈 Global Oil Price Trend")

    st.plotly_chart(

        line_chart(

            yearly,

            "Year",

            "Average_Oil_Price",

            "Oil Price Trend",

            "#3B82F6"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Highest Oil Price Years
    # ============================================================

    highest = (

        yearly

        .sort_values(

            "Average_Oil_Price",

            ascending=False

        )

        .head(15)

    )

    st.subheader("🔥 Highest Oil Price Years")

    st.plotly_chart(

        horizontal_bar_chart(

            highest,

            "Average_Oil_Price",

            "Year",

            "Highest Oil Price Years"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Distribution
    # ============================================================

    hist_df = pd.DataFrame({

        "Oil Price":

        master["Average_Oil_Price"]

    })

    st.subheader("📊 Oil Price Distribution")

    st.plotly_chart(

        histogram_chart(

            hist_df,

            "Oil Price",

            "Oil Price Distribution"

        ),

        use_container_width=True

    )

    st.divider()


    # ============================================================
    # Rolling Average
    # ============================================================

    oil = yearly.copy()

    oil["Rolling_Average"] = (

        oil["Average_Oil_Price"]

        .rolling(window=3)

        .mean()

    )

    st.subheader("📉 3-Year Rolling Average")

    import plotly.express as px

    fig = px.line(

        oil,

        x="Year",

        y=["Average_Oil_Price", "Rolling_Average"],

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
    # Year-over-Year Change
    # ============================================================

    oil["Price_Change"] = (

        oil["Average_Oil_Price"]

        .diff()

    )

    st.subheader("📈 Year-over-Year Oil Price Change")

    st.plotly_chart(

        bar_chart(

            oil,

            "Year",

            "Price_Change",

            "Annual Oil Price Change"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Oil Price Volatility
    # ============================================================

    oil["Volatility (%)"] = (

        oil["Average_Oil_Price"]

        .pct_change()

        * 100

    )

    st.subheader("🌍 Oil Price Volatility")

    st.plotly_chart(

        line_chart(

            oil,

            "Year",

            "Volatility (%)",

            "Oil Price Volatility",

            "#EF4444"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Summary Table
    # ============================================================

    st.subheader("📋 Oil Price Summary")

    st.dataframe(

        oil,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Executive Insights
    # ============================================================

    highest_year = yearly.loc[
        yearly["Average_Oil_Price"].idxmax(),
        "Year"
    ]

    lowest_year = yearly.loc[
        yearly["Average_Oil_Price"].idxmin(),
        "Year"
    ]

    st.subheader("📌 Executive Insights")

    st.success(f"""

### Oil Market Summary

🛢 Average Oil Price :
**${avg_price:.2f}**

📈 Highest Oil Price :
**${highest_price:.2f} ({int(highest_year)})**

📉 Lowest Oil Price :
**${lowest_price:.2f} ({int(lowest_year)})**

📅 Years Covered :
**{master['Year'].min()} - {master['Year'].max()}**

""")

    st.divider()

    # ============================================================
    # Download Dataset
    # ============================================================

    st.subheader("📥 Download Dataset")

    st.download_button(

        label="⬇ Download Oil Dataset",

        data=master.to_csv(index=False),

        file_name="oil_dashboard.csv",

        mime="text/csv"

    )

    st.divider()

    # ============================================================
    # Footer
    # ============================================================

    st.markdown(
        """
---
### 🛢 Oil Price Analysis Dashboard

Developed using **Python • Pandas • Plotly • Streamlit**
"""
    )
