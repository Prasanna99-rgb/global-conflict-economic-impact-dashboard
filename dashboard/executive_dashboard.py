# ============================================================
# Executive Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart,
    correlation_heatmap
)


def show_executive_dashboard(master, impact):

    st.title("🌍 Executive Dashboard")

    st.markdown(
        "Analyze global conflicts and their impact on military spending, inflation, and oil prices."
    )

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    total_conflicts = int(master["Conflict_Count"].sum())

    countries = master["Country Name"].nunique()

    avg_military = master["Military_Spending"].mean()

    avg_inflation = master["Inflation_Rate"].mean()

    avg_oil = master["Average_Oil_Price"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "⚔️ Total Conflicts",
        f"{total_conflicts:,}"
    )

    c2.metric(
        "🌍 Countries",
        countries
    )

    c3.metric(
        "🪖 Avg Military",
        f"{avg_military:,.2f}"
    )

    c4.metric(
        "📈 Avg Inflation",
        f"{avg_inflation:.2f}%"
    )

    c5.metric(
        "🛢 Avg Oil",
        f"${avg_oil:.2f}"
    )

    st.divider()

    # ============================================================
    # Conflict Trend
    # ============================================================

    left, right = st.columns(2)

    with left:

        yearly_conflict = (

            master

            .groupby("Year")["Conflict_Count"]

            .sum()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                yearly_conflict,

                "Year",

                "Conflict_Count",

                "Global Conflict Trend",

                "#FF4B4B"

            ),

            use_container_width=True

        )

    # ============================================================
    # Military Trend
    # ============================================================

    with right:

        military = (

            master

            .groupby("Year")["Military_Spending"]

            .mean()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                military,

                "Year",

                "Military_Spending",

                "Military Spending Trend",

                "#00CC96"

            ),

            use_container_width=True

        )

    # ============================================================
    # Inflation
    # ============================================================

    left, right = st.columns(2)

    with left:

        inflation = (

            master

            .groupby("Year")["Inflation_Rate"]

            .mean()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                inflation,

                "Year",

                "Inflation_Rate",

                "Inflation Trend",

                "#FFA500"

            ),

            use_container_width=True

        )

    # ============================================================
    # Oil Trend
    # ============================================================

    with right:

        oil = (

            master

            .groupby("Year")["Average_Oil_Price"]

            .mean()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                oil,

                "Year",

                "Average_Oil_Price",

                "Oil Price Trend",

                "#3399FF"

            ),

            use_container_width=True

        )

    st.divider()

    # ============================================================
    # Top Impacted Countries
    # ============================================================

    st.subheader("🌍 Top 15 Most Impacted Countries")

    top15 = (

        impact

        .sort_values(

            "Impact_Score",

            ascending=False

        )

        .head(15)

    )

    st.plotly_chart(

        bar_chart(

            top15,

            "Country Name",

            "Impact_Score",

            "Impact Score Ranking"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Correlation Heatmap
    # ============================================================

    st.subheader("📊 Correlation Analysis")

    corr = master[

        [

            "Conflict_Count",

            "Average_Intensity",

            "Military_Spending",

            "Inflation_Rate",

            "Average_Oil_Price"

        ]

    ].corr()

    st.plotly_chart(

        correlation_heatmap(corr),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Dashboard Insights
    # ============================================================

    st.subheader("📌 Executive Insights")

    highest_country = impact.sort_values(
        "Impact_Score",
        ascending=False
    ).iloc[0]["Country Name"]

    st.success(f"""
• Total conflict records analysed: **{total_conflicts:,}**

• Countries analysed: **{countries}**

• Country with highest overall impact: **{highest_country}**

• Dashboard integrates:
    - Global Conflict Data
    - Military Spending
    - Inflation
    - Oil Prices
""")
