# ============================================================
# Inflation Dashboard
# Part 1
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart
)


def show_inflation_dashboard(master):

    st.title("📈 Inflation Analysis Dashboard")

    st.markdown("""
    Analyze inflation trends across countries and compare
    inflation over time.
    """)

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    avg_inflation = master["Inflation_Rate"].mean()

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

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📈 Average Inflation",
        f"{avg_inflation:.2f}%"
    )

    c2.metric(
        "🔥 Highest Inflation",
        highest_country
    )

    c3.metric(
        "❄️ Lowest Inflation",
        lowest_country
    )

    c4.metric(
        "🌍 Countries",
        master["Country Name"].nunique()
    )

    st.divider()

    # ============================================================
    # Global Inflation Trend
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

            "Average Global Inflation",

            "#FFA500"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Highest Inflation Countries
    # ============================================================

    st.subheader("🔥 Top 15 Inflation Countries")

    top_country = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .sort_values(ascending=False)

        .head(15)

        .reset_index()

    )

    st.plotly_chart(

        bar_chart(

            top_country,

            "Country Name",

            "Inflation_Rate",

            "Highest Inflation Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Lowest Inflation Countries
    # ============================================================

    st.subheader("❄️ Lowest Inflation Countries")

    low_country = (

        master

        .groupby("Country Name")["Inflation_Rate"]

        .mean()

        .sort_values()

        .head(15)

        .reset_index()

    )

    st.plotly_chart(

        bar_chart(

            low_country,

            "Country Name",

            "Inflation_Rate",

            "Lowest Inflation Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Yearly Table
    # ============================================================

    st.subheader("📅 Inflation Summary")

    st.dataframe(

        yearly,

        use_container_width=True,

        hide_index=True

    )



    # ============================================================
    # Inflation Distribution
    # ============================================================

    st.subheader("📊 Inflation Rate Distribution")

    st.bar_chart(
        master["Inflation_Rate"].dropna().value_counts(bins=20)
    )

    st.divider()

    # ============================================================
    # Country Comparison
    # ============================================================

    st.subheader("🌍 Compare Inflation Between Countries")

    countries = sorted(
        master["Country Name"].dropna().unique()
    )

    selected = st.multiselect(

        "Select Countries",

        countries,

        default=countries[:3]

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

        title="Inflation Comparison"

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

    st.subheader("📈 Inflation Volatility")

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

    fig = px.bar(

        volatility,

        x="Country Name",

        y="Inflation_Rate",

        title="Countries with Highest Inflation Volatility",

        color="Inflation_Rate",

        color_continuous_scale="Oranges"

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

    ranking["Rank"] = ranking.index + 1

    ranking = ranking[

        [

            "Rank",

            "Country Name",

            "Inflation_Rate"

        ]

    ]

    st.dataframe(

        ranking,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Business Insights
    # ============================================================

    st.subheader("📌 Inflation Insights")

    st.success(f"""

### Key Findings

• Countries Analysed : **{master['Country Name'].nunique()}**

• Years Covered : **{master['Year'].min()} - {master['Year'].max()}**

• Highest Inflation Country :

**{highest_country}**

• Highest Inflation Rate :

**{highest_rate:.2f}%**

• Lowest Inflation Country :

**{lowest_country}**

• Lowest Inflation Rate :

**{lowest_rate:.2f}%**

• Average Inflation :

**{avg_inflation:.2f}%**

""")

    st.divider()

    # ============================================================
    # Download Dataset
    # ============================================================

    st.download_button(

        "📥 Download Inflation Dataset",

        data=master.to_csv(index=False),

        file_name="inflation_dashboard.csv",

        mime="text/csv"

    )
