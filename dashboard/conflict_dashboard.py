# ============================================================
# Conflict Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    line_chart,
    bar_chart,
    horizontal_bar_chart,
    pie_chart
)


def show_conflict_dashboard(master):

    conflict_df = pd.read_csv(
        "Data_Processed/clean_conflict.csv"
    )

    st.title("⚔️ Global Conflict Analysis")

    st.markdown("""
Explore worldwide armed conflicts using historical conflict data.
""")

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    total_conflicts = len(conflict_df)

    countries = conflict_df["location"].nunique()

    regions = conflict_df["region"].nunique()

    avg_intensity = round(
        conflict_df["intensity_level"].mean(),
        2
    )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "⚔️ Conflict Records",
        f"{total_conflicts:,}"
    )

    c2.metric(
        "🌍 Countries",
        countries
    )

    c3.metric(
        "🌎 Regions",
        regions
    )

    c4.metric(
        "🔥 Avg Intensity",
        avg_intensity
    )

    st.divider()

    # ============================================================
    # Conflict Trend
    # ============================================================

    yearly = (

        conflict_df

        .groupby("year")

        .size()

        .reset_index(name="Conflict_Count")

    )

    st.subheader("📈 Global Conflict Trend")

    st.plotly_chart(

        line_chart(

            yearly,

            "year",

            "Conflict_Count",

            "Conflict Trend",

            "#EF4444"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Top Conflict Countries
    # ============================================================

    top_country = (

        conflict_df

        .groupby("location")

        .size()

        .reset_index(name="Conflict_Count")

        .sort_values(

            "Conflict_Count",

            ascending=False

        )

        .head(15)

    )

    st.subheader("🌍 Top 15 Conflict Countries")

    st.plotly_chart(

        horizontal_bar_chart(

            top_country,

            "Conflict_Count",

            "location",

            "Most Conflict-Affected Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Conflict Severity
    # ============================================================

    severity = (

        conflict_df

        .groupby("intensity_level")

        .size()

        .reset_index(name="Count")

    )

    st.subheader("🔥 Conflict Intensity Distribution")

    st.plotly_chart(

        pie_chart(

            severity,

            "intensity_level",

            "Count",

            "Conflict Intensity"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Region Analysis
    # ============================================================

    st.subheader("🌎 Conflicts by Region")

    region = (

        conflict_df

        .groupby("region")

        .size()

        .reset_index(name="Conflict_Count")

        .sort_values(

            "Conflict_Count",

            ascending=False

        )

    )

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(

            horizontal_bar_chart(

                region,

                "Conflict_Count",

                "region",

                "Conflict Distribution by Region"

            ),

            use_container_width=True

        )

    with col2:

        st.plotly_chart(

            pie_chart(

                region,

                "region",

                "Conflict_Count",

                "Regional Share"

            ),

            use_container_width=True

        )

    st.divider()

    # ============================================================
    # Conflict Type Analysis
    # ============================================================

    st.subheader("⚔️ Conflict Type Analysis")

    conflict_type = (

        conflict_df

        .groupby("type_of_conflict")

        .size()

        .reset_index(name="Count")

        .sort_values(

            "Count",

            ascending=False

        )

    )

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(

            bar_chart(

                conflict_type,

                "type_of_conflict",

                "Count",

                "Conflict Types"

            ),

            use_container_width=True

        )

    with col2:

        st.dataframe(

            conflict_type,

            use_container_width=True,

            hide_index=True

        )

    st.divider()

    # ============================================================
    # Side A Analysis
    # ============================================================

    st.subheader("👥 Top Side A Actors")

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

        horizontal_bar_chart(

            side_a,

            "Conflict_Count",

            "side_a",

            "Top Side A Actors"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Side B Analysis
    # ============================================================

    st.subheader("👥 Top Side B Actors")

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

        horizontal_bar_chart(

            side_b,

            "Conflict_Count",

            "side_b",

            "Top Side B Actors"

        ),

        use_container_width=True

    )

    st.divider()


    # ============================================================
    # Conflict Duration Analysis
    # ============================================================

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
        duration_df["ep_end_date"] -
        duration_df["start_date"]
    ).dt.days

    duration_df = duration_df.dropna(
        subset=["Conflict_Duration_Days"]
    )

    avg_duration = duration_df[
        "Conflict_Duration_Days"
    ].mean()

    st.metric(
        "Average Conflict Duration",
        f"{avg_duration:.0f} Days"
    )

    longest = (

        duration_df

        .sort_values(
            "Conflict_Duration_Days",
            ascending=False
        )

        .head(15)

    )

    st.plotly_chart(

        horizontal_bar_chart(

            longest,

            "Conflict_Duration_Days",

            "location",

            "Top 15 Longest Conflicts"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Top Conflict Years
    # ============================================================

    st.subheader("📅 Top Conflict Years")

    top_years = (

        conflict_df

        .groupby("year")

        .size()

        .reset_index(name="Conflict_Count")

        .sort_values(
            "Conflict_Count",
            ascending=False
        )

        .head(10)

    )

    st.dataframe(

        top_years,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Executive Insights
    # ============================================================

    st.subheader("📌 Conflict Insights")

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

### Key Findings

🌍 Countries Covered :
**{countries}**

🌎 Regions Covered :
**{regions}**

⚔️ Total Conflict Records :
**{total_conflicts:,}**

🔥 Most Affected Country :
**{highest_country}**

🌍 Most Affected Region :
**{highest_region}**

⚔️ Most Common Conflict Type :
**{common_type}**

⏳ Average Conflict Duration :
**{avg_duration:.0f} Days**

""")

    st.divider()

    # ============================================================
    # Download Dataset
    # ============================================================

    st.subheader("📥 Download Data")

    st.download_button(

        label="⬇ Download Conflict Dataset",

        data=conflict_df.to_csv(index=False),

        file_name="clean_conflict.csv",

        mime="text/csv"

    )

    st.divider()

    # ============================================================
    # Footer
    # ============================================================

    st.markdown(
        """
---
### ⚔️ Conflict Analysis Dashboard

**Data Source:** UCDP/PRIO Armed Conflict Dataset

Developed using **Python • Pandas • Plotly • Streamlit**
"""
    )
