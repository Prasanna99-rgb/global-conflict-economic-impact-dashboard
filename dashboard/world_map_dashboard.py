# ============================================================
# World Map Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import world_map


def show_world_map_dashboard(master):

    st.title("🌍 Global Interactive Map")

    st.markdown("""
Explore global conflicts and economic indicators using an interactive world map.
""")

    st.divider()

    # ============================================================
    # Select Metric
    # ============================================================

    metric = st.selectbox(

        "Select Metric",

        [

            "Conflict_Count",

            "Military_Spending",

            "Inflation_Rate",

            "Average_Oil_Price",

            "Average_Intensity"

        ]

    )

    country_data = (

        master

        .groupby("Country Name")

        .agg({

            "Conflict_Count":"sum",

            "Military_Spending":"mean",

            "Inflation_Rate":"mean",

            "Average_Oil_Price":"mean",

            "Average_Intensity":"mean"

        })

        .reset_index()

    )

    st.plotly_chart(

        world_map(

            country_data,

            "Country Name",

            metric,

            f"{metric} Across Countries"

        ),

        use_container_width=True

    )

    st.divider()

    st.dataframe(

        country_data,

        use_container_width=True,

        hide_index=True

    )



    # ============================================================
    # Top 15 Countries
    # ============================================================

    st.subheader(f"🏆 Top 15 Countries by {metric}")

    top15 = (

        country_data

        .sort_values(

            metric,

            ascending=False

        )

        .head(15)

    )

    st.dataframe(

        top15,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Download
    # ============================================================

    st.download_button(

        "⬇ Download World Map Data",

        data=country_data.to_csv(index=False),

        file_name="world_map_data.csv",

        mime="text/csv"

    )

    st.divider()

    st.markdown(
        """
---
### 🌍 Global Interactive Map

Visualize worldwide conflict and economic indicators using Plotly Choropleth Maps.
"""
    )
