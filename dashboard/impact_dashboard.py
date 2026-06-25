# ============================================================
# Global Impact Dashboard
# Part 1
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.charts import (
    scatter_chart,
    correlation_heatmap,
    bar_chart
)


def show_impact_dashboard(master):

    st.title("🌍 Global Impact Dashboard")

    st.markdown("""
Analyze how global conflicts influence

- Military Spending
- Inflation
- Oil Prices

using interactive visualizations.
""")

    st.divider()

    # ============================================================
    # KPI Cards
    # ============================================================

    total_conflicts = int(master["Conflict_Count"].sum())

    avg_military = master["Military_Spending"].mean()

    avg_inflation = master["Inflation_Rate"].mean()

    avg_oil = master["Average_Oil_Price"].mean()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "⚔️ Conflicts",
        f"{total_conflicts:,}"
    )

    c2.metric(
        "🪖 Avg Military",
        f"{avg_military:,.2f}"
    )

    c3.metric(
        "📈 Avg Inflation",
        f"{avg_inflation:.2f}%"
    )

    c4.metric(
        "🛢 Avg Oil",
        f"${avg_oil:.2f}"
    )

    st.divider()

    # ============================================================
    # Correlation Matrix
    # ============================================================

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

    # ============================================================
    # Conflict vs Military
    # ============================================================

    st.subheader("⚔️ Conflict vs Military Spending")

    st.plotly_chart(

        scatter_chart(

            master,

            "Conflict_Count",

            "Military_Spending",

            color="Conflict_Severity",

            hover="Country Name",

            title="Conflict vs Military Spending"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Conflict vs Inflation
    # ============================================================

    st.subheader("📈 Conflict vs Inflation")

    st.plotly_chart(

        scatter_chart(

            master,

            "Conflict_Count",

            "Inflation_Rate",

            color="Inflation_Level",

            hover="Country Name",

            title="Conflict vs Inflation"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Conflict vs Oil Price
    # ============================================================

    oil = (

        master

        .groupby("Year")

        .agg(

            {

                "Conflict_Count":"sum",

                "Average_Oil_Price":"mean"

            }

        )

        .reset_index()

    )

    fig = px.line(

        oil,

        x="Year",

        y=["Conflict_Count","Average_Oil_Price"],

        markers=True,

        title="Conflict vs Oil Price"

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
    # Top 20 Impacted Countries
    # ============================================================

    st.subheader("🌍 Top 20 Most Impacted Countries")

    impact = (

        master

        .groupby("Country Name")

        .agg(

            {

                "Conflict_Count":"sum",

                "Average_Intensity":"mean",

                "Military_Spending":"mean",

                "Inflation_Rate":"mean"

            }

        )

        .reset_index()

    )

    # ------------------------------------------------------------
    # Normalize Values
    # ------------------------------------------------------------

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()

    cols = [

        "Conflict_Count",

        "Average_Intensity",

        "Military_Spending",

        "Inflation_Rate"

    ]

    impact[cols] = scaler.fit_transform(

        impact[cols]

    )

    impact["Impact_Score"] = (

        0.35 * impact["Conflict_Count"] +

        0.30 * impact["Average_Intensity"] +

        0.20 * impact["Military_Spending"] +

        0.15 * impact["Inflation_Rate"]

    )

    impact = impact.sort_values(

        "Impact_Score",

        ascending=False

    )

    top20 = impact.head(20)

    st.plotly_chart(

        bar_chart(

            top20,

            "Country Name",

            "Impact_Score",

            "Top 20 Impacted Countries"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Ranking Table
    # ============================================================

    st.subheader("🏆 Global Impact Ranking")

    ranking = top20.copy()

    ranking["Rank"] = ranking.index + 1

    ranking = ranking[

        [

            "Rank",

            "Country Name",

            "Impact_Score"

        ]

    ]

    st.dataframe(

        ranking,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Yearly Summary
    # ============================================================

    st.subheader("📅 Global Yearly Summary")

    yearly = (

        master

        .groupby("Year")

        .agg(

            {

                "Conflict_Count":"sum",

                "Military_Spending":"mean",

                "Inflation_Rate":"mean",

                "Average_Oil_Price":"mean"

            }

        )

        .reset_index()

    )

    st.dataframe(

        yearly,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Global Metrics
    # ============================================================

    st.subheader("📈 Global Metrics")

    c1,c2,c3 = st.columns(3)

    with c1:

        st.metric(

            "Highest Impact Country",

            top20.iloc[0]["Country Name"]

        )

    with c2:

        st.metric(

            "Countries Analysed",

            master["Country Name"].nunique()

        )

    with c3:

        st.metric(

            "Years Covered",

            f"{master['Year'].min()} - {master['Year'].max()}"

        )

    st.divider()

    # ============================================================
    # Executive Insights
    # ============================================================

    st.subheader("📌 Executive Insights")

    st.success(f"""

### Global Findings

• Countries Analysed :
**{master['Country Name'].nunique()}**

• Total Conflict Records :
**{int(master['Conflict_Count'].sum()):,}**

• Highest Impact Country :
**{top20.iloc[0]['Country Name']}**

• Average Military Spending :
**{master['Military_Spending'].mean():,.2f}**

• Average Inflation :
**{master['Inflation_Rate'].mean():.2f}%**

• Average Oil Price :
**${master['Average_Oil_Price'].mean():.2f}**

""")

    st.divider()

    # ============================================================
    # Download Master Dataset
    # ============================================================

    st.download_button(

        label="📥 Download Master Dataset",

        data=master.to_csv(index=False),

        file_name="global_conflict_master_dataset.csv",

        mime="text/csv"

    )

    st.divider()

    # ============================================================
    # Footer
    # ============================================================

    st.markdown(
        """
        ---
        **Global Conflict & Economic Impact Dashboard**

        Developed using **Python • Pandas • Plotly • Streamlit**
        """
    )
