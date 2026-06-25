# ============================================================
# Military Spending Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart,
    horizontal_bar_chart,
    histogram_chart
)


def show_military_dashboard(master):

    st.title("🪖 Military Spending Dashboard")

    st.markdown("""
Analyze global military expenditure trends and compare spending across countries.
""")

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    total_spending = master["Military_Spending"].sum()

    avg_spending = master["Military_Spending"].mean()

    countries = master["Country Name"].nunique()

    highest_country = (

        master

        .groupby("Country Name")["Military_Spending"]

        .mean()

        .idxmax()

    )

    highest_spending = (

        master

        .groupby("Country Name")["Military_Spending"]

        .mean()

        .max()

    )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "💰 Total Spending",
        f"{total_spending:,.0f}"
    )

    c2.metric(
        "📊 Average Spending",
        f"{avg_spending:,.2f}"
    )

    c3.metric(
        "🌍 Countries",
        countries
    )

    c4.metric(
        "🏆 Highest Spending",
        highest_country
    )

    st.divider()

    # ============================================================
    # Global Trend
    # ============================================================

    yearly = (

        master

        .groupby("Year")["Military_Spending"]

        .mean()

        .reset_index()

    )

    st.subheader("📈 Global Military Spending Trend")

    st.plotly_chart(

        line_chart(

            yearly,

            "Year",

            "Military_Spending",

            "Military Spending Trend",

            "#10B981"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Top Spending Countries
    # ============================================================

    top_country = (

        master

        .groupby("Country Name")["Military_Spending"]

        .mean()

        .sort_values(

            ascending=False

        )

        .head(15)

        .reset_index()

    )

    st.subheader("🌍 Top 15 Military Spending Countries")

    st.plotly_chart(

        horizontal_bar_chart(

            top_country,

            "Military_Spending",

            "Country Name",

            "Top Military Spending Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Distribution
    # ============================================================

    st.subheader("📊 Spending Distribution")

    hist_df = pd.DataFrame({

        "Military Spending":

        master["Military_Spending"]

    })

    st.plotly_chart(

        histogram_chart(

            hist_df,

            "Military Spending",

            "Military Spending Distribution"

        ),

        use_container_width=True

    )

    st.divider()


    # ============================================================
    # Country Comparison
    # ============================================================

    st.subheader("🌍 Compare Military Spending")

    countries_list = sorted(
        master["Country Name"].dropna().unique()
    )

    selected = st.multiselect(

        "Select Countries",

        countries_list,

        default=countries_list[:3]

    )

    compare = master[
        master["Country Name"].isin(selected)
    ]

    compare = (

        compare

        .groupby(
            ["Year", "Country Name"]
        )["Military_Spending"]

        .mean()

        .reset_index()

    )

    import plotly.express as px

    fig = px.line(

        compare,

        x="Year",

        y="Military_Spending",

        color="Country Name",

        markers=True,

        title="Military Spending Comparison"

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
    # Fastest Growing Military Budgets
    # ============================================================

    growth = (

        master

        .groupby(
            ["Country Name", "Year"]
        )["Military_Spending"]

        .mean()

        .reset_index()

    )

    growth = growth.pivot(

        index="Country Name",

        columns="Year",

        values="Military_Spending"

    )

    growth["Growth"] = (

        growth.iloc[:, -1]

        -

        growth.iloc[:, 0]

    )

    growth = (

        growth

        .sort_values(
            "Growth",
            ascending=False
        )

        .head(15)

        .reset_index()

    )

    st.subheader("🚀 Fastest Growing Military Budgets")

    st.plotly_chart(

        horizontal_bar_chart(

            growth,

            "Growth",

            "Country Name",

            "Military Spending Growth"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Top Spending Ranking
    # ============================================================

    st.subheader("🏆 Military Spending Ranking")

    ranking = (

        master

        .groupby("Country Name")["Military_Spending"]

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

    st.success(f"""

### Military Spending Summary

🌍 Countries Covered :
**{countries}**

💰 Total Military Spending :
**{total_spending:,.0f}**

📊 Average Spending :
**{avg_spending:,.2f}**

🏆 Highest Spending Country :
**{highest_country}**

💵 Highest Average Spending :
**{highest_spending:,.2f}**

📅 Years Covered :
**{master['Year'].min()} - {master['Year'].max()}**

""")

    st.divider()

    # ============================================================
    # Download Dataset
    # ============================================================

    st.subheader("📥 Download Dataset")

    st.download_button(

        label="⬇ Download Military Dataset",

        data=master.to_csv(index=False),

        file_name="military_dashboard.csv",

        mime="text/csv"

    )

    st.divider()

    # ============================================================
    # Footer
    # ============================================================

    st.markdown(
        """
---
### 🪖 Military Spending Dashboard

Developed using **Python • Pandas • Plotly • Streamlit**
"""
    )
