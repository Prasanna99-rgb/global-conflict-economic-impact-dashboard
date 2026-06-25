# ============================================================
# Inflation Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    horizontal_bar_chart,
    histogram_chart
)


def show_inflation_dashboard(master):

    st.title("📈 Inflation Analysis Dashboard")

    st.markdown("""
Analyze inflation trends across countries and compare inflation over time.
""")

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    avg_inflation = master["Inflation_Rate"].mean()

    countries = master["Country Name"].nunique()

    highest_country = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .idxmax()

    )

    highest_rate = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .max()

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📈 Avg Inflation",
        f"{avg_inflation:.2f}%"
    )

    c2.metric(
        "🌍 Countries",
        countries
    )

    c3.metric(
        "🔥 Highest Inflation",
        highest_country
    )

    c4.metric(
        "📊 Peak Rate",
        f"{highest_rate:.2f}%"
    )

    st.divider()

    # ============================================================
    # Inflation Trend
    # ============================================================

    yearly = (

        master

        .groupby("Year")["Inflation_Rate"]

        .mean()

        .reset_index()

    )

    st.subheader("📈 Global Inflation Trend")

    st.plotly_chart(

        line_chart(

            yearly,

            "Year",

            "Inflation_Rate",

            "Average Inflation",

            "#F59E0B"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Top Inflation Countries
    # ============================================================

    top_country = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .sort_values(

            ascending=False

        )

        .head(15)

        .reset_index()

    )

    st.subheader("🌍 Highest Inflation Countries")

    st.plotly_chart(

        horizontal_bar_chart(

            top_country,

            "Inflation_Rate",

            "Country Name",

            "Highest Inflation Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Distribution
    # ============================================================

    hist_df = pd.DataFrame({

        "Inflation Rate":

        master["Inflation_Rate"]

    })

    st.subheader("📊 Inflation Distribution")

    st.plotly_chart(

        histogram_chart(

            hist_df,

            "Inflation Rate",

            "Inflation Distribution"

        ),

        use_container_width=True

    )

    st.divider()


    # ============================================================
    # Country Comparison
    # ============================================================

    st.subheader("🌍 Compare Inflation Between Countries")

    country_list = sorted(
        master["Country Name"].dropna().unique()
    )

    selected = st.multiselect(

        "Select Countries",

        country_list,

        default=country_list[:3]

    )

    compare = master[
        master["Country Name"].isin(selected)
    ]

    compare = (

        compare

        .groupby(
            ["Year", "Country Name"]
        )["Inflation_Rate"]

        .mean()

        .reset_index()

    )

    import plotly.express as px

    fig = px.line(

        compare,

        x="Year",

        y="Inflation_Rate",

        color="Country Name",

        markers=True,

        title="Country Inflation Comparison"

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
    # Inflation Volatility
    # ============================================================

    volatility = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .std()

        .reset_index()

        .sort_values(

            "Inflation_Rate",

            ascending=False

        )

        .head(15)

    )

    st.subheader("📉 Highest Inflation Volatility")

    st.plotly_chart(

        horizontal_bar_chart(

            volatility,

            "Inflation_Rate",

            "Country Name",

            "Inflation Volatility"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Inflation Ranking
    # ============================================================

    st.subheader("🏆 Inflation Ranking")

    ranking = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )

    ranking.index = ranking.index + 1

    st.dataframe(

        ranking,

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Executive Insights
    # ============================================================

    st.subheader("📌 Executive Insights")

    lowest_country = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .idxmin()

    )

    lowest_rate = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .min()

    )

    st.success(f"""

### Inflation Summary

🌍 Countries Covered :
**{countries}**

📈 Average Inflation :
**{avg_inflation:.2f}%**

🔥 Highest Inflation Country :
**{highest_country}**

🔥 Highest Inflation Rate :
**{highest_rate:.2f}%**

❄️ Lowest Inflation Country :
**{lowest_country}**

❄️ Lowest Inflation Rate :
**{lowest_rate:.2f}%**

📅 Years Covered :
**{master['Year'].min()} - {master['Year'].max()}**

""")

    st.divider()

    # ============================================================
    # Download Dataset
    # ============================================================

    st.subheader("📥 Download Dataset")

    st.download_button(

        label="⬇ Download Inflation Dataset",

        data=master.to_csv(index=False),

        file_name="inflation_dashboard.csv",

        mime="text/csv"

    )

    st.divider()

    # ============================================================
    # Footer
    # ============================================================

    st.markdown(
        """
---
### 📈 Inflation Analysis Dashboard

Developed using **Python • Pandas • Plotly • Streamlit**
"""
    )
