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

    # ========================================================
    # Load Original Conflict Dataset
    # ========================================================

    conflict_df = pd.read_csv(
        "Data_Processed/clean_conflict.csv"
    )

    # ========================================================
    # Regional Conflict Analysis
    # ========================================================

    st.subheader("🌍 Conflicts by Region")

    region_data = (

        conflict_df

        .groupby("region")

        .size()

        .reset_index(name="Conflict_Count")

        .sort_values(
            "Conflict_Count",
            ascending=False
        )

    )

    st.plotly_chart(

        bar_chart(

            region_data,

            "region",

            "Conflict_Count",

            "Regional Conflict Distribution"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Conflict Type Analysis
    # ========================================================

    st.subheader("⚔️ Conflict Type Distribution")

    type_data = (

        conflict_df

        .groupby("type_of_conflict")

        .size()

        .reset_index(name="Count")

    )

    st.plotly_chart(

        bar_chart(

            type_data,

            "type_of_conflict",

            "Count",

            "Conflict Types"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Intensity Level Distribution
    # ========================================================

    st.subheader("🔥 Conflict Intensity")

    intensity = (

        conflict_df

        .groupby("intensity_level")

        .size()

        .reset_index(name="Count")

    )

    st.plotly_chart(

        bar_chart(

            intensity,

            "intensity_level",

            "Count",

            "Conflict Intensity Levels"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Top 10 Regions
    # ========================================================

    st.subheader("🌎 Top Conflict Regions")

    st.dataframe(

        region_data.head(10),

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ========================================================
    # Conflict Type Table
    # ========================================================

    st.subheader("📊 Conflict Type Summary")

    st.dataframe(

        type_data,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ========================================================
    # Average Intensity By Region
    # ========================================================

    st.subheader("📈 Average Conflict Intensity by Region")

    avg_region = (

        conflict_df

        .groupby("region")["intensity_level"]

        .mean()

        .reset_index()

        .sort_values(
            "intensity_level",
            ascending=False
        )

    )

    st.plotly_chart(

        bar_chart(

            avg_region,

            "region",

            "intensity_level",

            "Average Intensity"

        ),

        use_container_width=True

    )

    st.divider()



    # ========================================================
    # Side A Analysis
    # ========================================================

    st.subheader("👥 Top 15 Side A Actors")

    side_a = (

        conflict_df

        .groupby("side_a")

        .size()

        .reset_index(name="Conflict_Count")

        .sort_values(
            "Conflict_Count",
            ascending=False
        )

        .head(15)

    )

    st.plotly_chart(

        bar_chart(

            side_a,

            "side_a",

            "Conflict_Count",

            "Top Side A Actors"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Side B Analysis
    # ========================================================

    st.subheader("👥 Top 15 Side B Actors")

    side_b = (

        conflict_df

        .groupby("side_b")

        .size()

        .reset_index(name="Conflict_Count")

        .sort_values(
            "Conflict_Count",
            ascending=False
        )

        .head(15)

    )

    st.plotly_chart(

        bar_chart(

            side_b,

            "side_b",

            "Conflict_Count",

            "Top Side B Actors"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Conflict Duration
    # ========================================================

    st.subheader("⏳ Conflict Duration Analysis")

    duration_df = conflict_df.copy()

    duration_df["start_date"] = pd.to_datetime(
        duration_df["start_date"],
        errors="coerce"
    )

    duration_df["ep_end_date"] = pd.to_datetime(
        duration_df["ep_end_date"],
        errors="coerce"
    )

    duration_df["Conflict_Duration_Days"] = (

        duration_df["ep_end_date"]

        -

        duration_df["start_date"]

    ).dt.days

    duration_df = duration_df.dropna(
        subset=["Conflict_Duration_Days"]
    )

    st.metric(

        "Average Duration (Days)",

        f"{duration_df['Conflict_Duration_Days'].mean():.0f}"

    )

    st.plotly_chart(

        bar_chart(

            duration_df

            .sort_values(
                "Conflict_Duration_Days",
                ascending=False
            )

            .head(15),

            "location",

            "Conflict_Duration_Days",

            "Longest Conflicts"

        ),

        use_container_width=True

    )

    st.divider()

    # ========================================================
    # Longest Conflicts Table
    # ========================================================

    st.subheader("📅 Top 15 Longest Conflicts")

    longest = (

        duration_df

        [

            [

                "location",

                "side_a",

                "side_b",

                "Conflict_Duration_Days"

            ]

        ]

        .sort_values(

            "Conflict_Duration_Days",

            ascending=False

        )

        .head(15)

    )

    st.dataframe(

        longest,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ========================================================
    # Business Insights
    # ========================================================

    st.subheader("📌 Key Insights")

    highest_country = (

        conflict_df["location"]

        .value_counts()

        .idxmax()

    )

    highest_region = (

        conflict_df["region"]

        .value_counts()

        .idxmax()

    )

    common_type = (

        conflict_df["type_of_conflict"]

        .mode()[0]

    )

    st.success(f"""

### Dashboard Summary

• Total Conflict Records : **{len(conflict_df):,}**

• Countries Covered : **{conflict_df['location'].nunique()}**

• Regions Covered : **{conflict_df['region'].nunique()}**

• Most Affected Country : **{highest_country}**

• Most Affected Region : **{highest_region}**

• Most Common Conflict Type : **{common_type}**

• Average Conflict Duration : **{duration_df['Conflict_Duration_Days'].mean():.0f} Days**

""")

    st.divider()

    # ========================================================
    # Download Dataset
    # ========================================================

    st.download_button(

        label="📥 Download Conflict Dataset",

        data=conflict_df.to_csv(index=False),

        file_name="conflict_dashboard.csv",

        mime="text/csv"

    )
