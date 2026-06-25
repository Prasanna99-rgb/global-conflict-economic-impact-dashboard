# ============================================================
# Executive Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart,
    horizontal_bar_chart,
    correlation_heatmap
)


def show_executive_dashboard(master, impact):

    # ========================================================
    # Header
    # ========================================================

    st.title("🌍 Global Conflict & Economic Impact Dashboard")

    st.markdown("""
Welcome to the **Executive Dashboard**.

This dashboard provides a high-level overview of:

- ⚔️ Global Conflicts
- 🪖 Military Spending
- 📈 Inflation
- 🛢 Oil Prices
- 🌍 Country Impact Analysis
""")

    st.divider()

    # ========================================================
    # Calculate KPIs
    # ========================================================

    total_conflicts = int(master["Conflict_Count"].sum())

    total_countries = master["Country Name"].nunique()

    avg_military = master["Military_Spending"].mean()

    avg_inflation = master["Inflation_Rate"].mean()

    avg_oil = master["Average_Oil_Price"].mean()

    highest_country = (

        impact

        .sort_values(

            "Impact_Score",

            ascending=False

        )

        .iloc[0]["Country Name"]

    )

    # ========================================================
    # KPI Cards
    # ========================================================

    c1, c2, c3 = st.columns(3)

    c4, c5, c6 = st.columns(3)

    with c1:

        st.metric(

            "⚔️ Total Conflicts",

            f"{total_conflicts:,}"

        )

    with c2:

        st.metric(

            "🌍 Countries",

            total_countries

        )

    with c3:

        st.metric(

            "🪖 Avg Military Spending",

            f"{avg_military:,.2f}"

        )

    with c4:

        st.metric(

            "📈 Avg Inflation",

            f"{avg_inflation:.2f}%"

        )

    with c5:

        st.metric(

            "🛢 Avg Oil Price",

            f"${avg_oil:.2f}"

        )

    with c6:

        st.metric(

            "🏆 Highest Impact",

            highest_country

        )

    st.divider()

    # ========================================================
    # Dashboard Overview
    # ========================================================

    st.subheader("📌 Dashboard Overview")

    st.info("""

This dashboard integrates multiple datasets to analyze
the relationship between:

• Global Conflicts

• Military Spending

• Inflation

• Oil Prices

Use the navigation menu to explore detailed dashboards.

""")

    st.divider()


    # ========================================================
    # Conflict Trend & Military Spending Trend
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("⚔️ Global Conflict Trend")

        conflict_trend = (

            master

            .groupby("Year")["Conflict_Count"]

            .sum()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                conflict_trend,

                "Year",

                "Conflict_Count",

                "Global Conflict Trend",

                "#EF4444"

            ),

            use_container_width=True

        )

    with col2:

        st.subheader("🪖 Military Spending Trend")

        military_trend = (

            master

            .groupby("Year")["Military_Spending"]

            .mean()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                military_trend,

                "Year",

                "Military_Spending",

                "Military Spending Trend",

                "#10B981"

            ),

            use_container_width=True

        )

    st.divider()

    # ========================================================
    # Inflation Trend & Oil Price Trend
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Inflation Trend")

        inflation_trend = (

            master

            .groupby("Year")["Inflation_Rate"]

            .mean()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                inflation_trend,

                "Year",

                "Inflation_Rate",

                "Average Inflation",

                "#F59E0B"

            ),

            use_container_width=True

        )

    with col2:

        st.subheader("🛢 Oil Price Trend")

        oil_trend = (

            master

            .groupby("Year")["Average_Oil_Price"]

            .mean()

            .reset_index()

        )

        st.plotly_chart(

            line_chart(

                oil_trend,

                "Year",

                "Average_Oil_Price",

                "Average Oil Price",

                "#3B82F6"

            ),

            use_container_width=True

        )

    st.divider()

    # ========================================================
    # Top Impact Countries
    # ========================================================

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

        horizontal_bar_chart(

            top15,

            "Impact_Score",

            "Country Name",

            "Top Impact Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Correlation Matrix
    # ========================================================

    st.subheader("📊 Correlation Matrix")

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

    # ========================================================
    # Executive Insights
    # ========================================================

    st.subheader("📌 Executive Insights")

    col1, col2 = st.columns([2, 1])

    with col1:

        st.success(f"""
### Global Overview

🌍 Countries Covered : **{total_countries}**

⚔️ Total Conflict Records : **{total_conflicts:,}**

🪖 Average Military Spending : **{avg_military:,.2f}**

📈 Average Inflation : **{avg_inflation:.2f}%**

🛢 Average Oil Price : **${avg_oil:.2f}**

🏆 Highest Impact Country : **{highest_country}**
""")

    with col2:

        latest_year = master["Year"].max()

        earliest_year = master["Year"].min()

        st.info(f"""
### Dataset Summary

📅 Period

**{earliest_year} - {latest_year}**

🌍 Countries

**{total_countries}**

📊 Records

**{len(master):,}**
""")

    st.divider()

    # ========================================================
    # Top 10 Countries Table
    # ========================================================

    st.subheader("🏆 Top 10 Countries by Impact Score")

    ranking = (

        impact

        .sort_values(

            "Impact_Score",

            ascending=False

        )

        .head(10)

        .reset_index(drop=True)

    )

    ranking.index = ranking.index + 1

    st.dataframe(

        ranking,

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Download Section
    # ========================================================

    st.subheader("📥 Download Data")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(

            label="⬇ Download Master Dataset",

            data=master.to_csv(index=False),

            file_name="global_conflict_master_dataset.csv",

            mime="text/csv"

        )

    with col2:

        st.download_button(

            label="⬇ Download Impact Dataset",

            data=impact.to_csv(index=False),

            file_name="country_impact_analysis.csv",

            mime="text/csv"

        )

    st.divider()

    # ========================================================
    # Footer
    # ========================================================

    st.markdown(
        """
---
### 🌍 Global Conflict & Economic Impact Dashboard

**Technologies Used**

- Python
- Pandas
- Plotly
- Streamlit
- Scikit-learn

Developed as an end-to-end **Data Analytics Portfolio Project**.
"""
    )
