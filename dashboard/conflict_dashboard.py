# ============================================================
# Conflict Dashboard
# Part 1
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart
)


def show_conflict_dashboard(master):

    st.title("⚔️ Global Conflict Analysis")

    st.markdown(
        """
Explore worldwide conflict trends, affected countries,
regions and conflict intensity over time.
"""
    )

    st.divider()

    # ========================================================
    # KPI Cards
    # ========================================================

    total_conflicts = int(master["Conflict_Count"].sum())

    countries = master["Country Name"].nunique()

    avg_intensity = round(
        master["Average_Intensity"].mean(),
        2
    )

    severe_conflicts = int(

        master[
            master["Conflict_Severity"] == "Extreme"
        ].shape[0]

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "⚔️ Conflict Records",
        f"{total_conflicts:,}"
    )

    c2.metric(
        "🌍 Countries",
        countries
    )

    c3.metric(
        "🔥 Avg Intensity",
        avg_intensity
    )

    c4.metric(
        "🚨 Extreme Conflicts",
        severe_conflicts
    )

    st.divider()

    # ========================================================
    # Yearly Conflict Trend
    # ========================================================

    yearly = (

        master

        .groupby("Year")["Conflict_Count"]

        .sum()

        .reset_index()

    )

    st.subheader("📈 Conflict Trend Over Time")

    st.plotly_chart(

        line_chart(

            yearly,

            "Year",

            "Conflict_Count",

            "Global Conflict Trend",

            "#FF4B4B"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Top Conflict Countries
    # ========================================================

    st.subheader("🌍 Top 15 Conflict Countries")

    top_country = (

        master

        .groupby("Country Name")

        ["Conflict_Count"]

        .sum()

        .sort_values(ascending=False)

        .head(15)

        .reset_index()

    )

    st.plotly_chart(

        bar_chart(

            top_country,

            "Country Name",

            "Conflict_Count",

            "Countries with Highest Conflict Records"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Top 10 Years
    # ========================================================

    st.subheader("📅 Top 10 Conflict Years")

    top_years = (

        yearly

        .sort_values(

            "Conflict_Count",

            ascending=False

        )

        .head(10)

    )

    st.dataframe(

        top_years,

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Conflict Severity Distribution
    # ========================================================

    st.subheader("🔥 Conflict Severity Distribution")

    severity = (

        master

        ["Conflict_Severity"]

        .value_counts()

        .reset_index()

    )

    severity.columns = [

        "Severity",

        "Count"

    ]

    st.plotly_chart(

        bar_chart(

            severity,

            "Severity",

            "Count",

            "Conflict Severity"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Yearly Table
    # ========================================================

    st.subheader("📊 Yearly Summary")

    st.dataframe(

        yearly,

        use_container_width=True,

        hide_index=True

    )
