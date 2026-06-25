# ============================================================
# Military Spending Dashboard
# Part 1
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart
)


def show_military_dashboard(master):

    st.title("🪖 Military Spending Dashboard")

    st.markdown("""
    Analyze military expenditure trends across countries
    and compare spending over time.
    """)

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    total_spending = master["Military_Spending"].sum()

    avg_spending = master["Military_Spending"].mean()

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

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Total Spending",
        f"{total_spending:,.0f}"
    )

    c2.metric(
        "📊 Average Spending",
        f"{avg_spending:,.2f}"
    )

    c3.metric(
        "🏆 Highest Spending Country",
        highest_country
    )

    c4.metric(
        "💵 Highest Average",
        f"{highest_spending:,.2f}"
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

            "Global Military Spending",

            "#00CC96"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Top Spending Countries
    # ============================================================

    st.subheader("🌍 Top 15 Military Spending Countries")

    top_country = (

        master

        .groupby("Country Name")["Military_Spending"]

        .mean()

        .sort_values(ascending=False)

        .head(15)

        .reset_index()

    )

    st.plotly_chart(

        bar_chart(

            top_country,

            "Country Name",

            "Military_Spending",

            "Top Military Spending Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Yearly Summary
    # ============================================================

    st.subheader("📅 Yearly Spending Summary")

    st.dataframe(

        yearly,

        use_container_width=True,

        hide_index=True

    )



    # ============================================================
    # Military Spending Distribution
    # ============================================================

    st.subheader("📊 Military Spending Distribution")

    spending_distribution = master["Military_Spending"].dropna()

    st.bar_chart(
        spending_distribution.value_counts(bins=20)
    )

    st.divider()

    # ============================================================
    # Country Comparison
    # ============================================================

    st.subheader("🌍 Compare Countries")

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

            ["Year","Country Name"]

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
    # Highest Spending Countries Table
    # ============================================================

    st.subheader("🏆 Highest Military Spending Countries")

    ranking = (

        master

        .groupby("Country Name")["Military_Spending"]

        .mean()

        .sort_values(ascending=False)

        .reset_index()

    )

    ranking["Rank"] = ranking.index + 1

    ranking = ranking[
        [
            "Rank",
            "Country Name",
            "Military_Spending"
        ]
    ]

    st.dataframe(

        ranking,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Spending Growth
    # ============================================================

    st.subheader("🚀 Spending Growth")

    growth = (

        master

        .groupby(
            ["Country Name","Year"]
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

        growth.iloc[:,-1]

        -

        growth.iloc[:,0]

    )

    growth = growth.sort_values(

        "Growth",

        ascending=False

    ).head(15)

    growth = growth.reset_index()

    fig = px.bar(

        growth,

        x="Country Name",

        y="Growth",

        title="Fastest Growing Military Budgets"

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
    # Business Insights
    # ============================================================

    st.subheader("📌 Military Spending Insights")

    st.success(f"""

• Countries Analysed : **{master['Country Name'].nunique()}**

• Years Covered : **{master['Year'].min()} - {master['Year'].max()}**

• Highest Spending Country :

**{highest_country}**

• Average Military Spending :

**{avg_spending:,.2f}**

• Highest Average Spending :

**{highest_spending:,.2f}**

""")

    st.divider()

    # ============================================================
    # Download Dataset
    # ============================================================

    st.download_button(

        "📥 Download Military Dataset",

        data=master.to_csv(index=False),

        file_name="military_dashboard.csv",

        mime="text/csv"

    )
