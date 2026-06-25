# ============================================================
# Global Impact Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from utils.charts import (
    scatter_chart,
    correlation_heatmap,
    horizontal_bar_chart
)


def show_impact_dashboard(master):

    st.title("🌍 Global Impact Dashboard")

    st.markdown("""
Analyze how conflicts influence military spending, inflation and oil prices across the world.
""")

    st.divider()

    # ============================================================
    # Create Impact Score
    # ============================================================

    impact = (

        master

        .groupby("Country Name")

        .agg({

            "Conflict_Count":"sum",

            "Average_Intensity":"mean",

            "Military_Spending":"mean",

            "Inflation_Rate":"mean",

            "Average_Oil_Price":"mean"

        })

        .reset_index()

    )

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()

    cols = [

        "Conflict_Count",

        "Average_Intensity",

        "Military_Spending",

        "Inflation_Rate",

        "Average_Oil_Price"

    ]

    impact[cols] = scaler.fit_transform(

        impact[cols]

    )

    impact["Impact_Score"] = (

        impact["Conflict_Count"]*0.35 +

        impact["Average_Intensity"]*0.25 +

        impact["Military_Spending"]*0.20 +

        impact["Inflation_Rate"]*0.10 +

        impact["Average_Oil_Price"]*0.10

    )

    # ============================================================
    # KPI Cards
    # ============================================================

    total_countries = impact.shape[0]

    highest_country = (

        impact

        .sort_values(

            "Impact_Score",

            ascending=False

        )

        .iloc[0]["Country Name"]

    )

    avg_score = impact["Impact_Score"].mean()

    max_score = impact["Impact_Score"].max()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "🌍 Countries",
        total_countries
    )

    c2.metric(
        "🏆 Highest Impact",
        highest_country
    )

    c3.metric(
        "📊 Avg Score",
        f"{avg_score:.3f}"
    )

    c4.metric(
        "🔥 Max Score",
        f"{max_score:.3f}"
    )

    st.divider()

    # ============================================================
    # Top Impact Countries
    # ============================================================

    top20 = (

        impact

        .sort_values(

            "Impact_Score",

            ascending=False

        )

        .head(20)

    )

    st.subheader("🌍 Top 20 Impacted Countries")

    st.plotly_chart(

        horizontal_bar_chart(

            top20,

            "Impact_Score",

            "Country Name",

            "Impact Score Ranking"

        ),

        use_container_width=True

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

        correlation_heatmap(

            corr

        ),

        use_container_width=True

    )

    st.divider()



    # ============================================================
    # Conflict vs Military Spending
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

    st.subheader("🛢 Conflict vs Oil Price")

    st.plotly_chart(

        scatter_chart(

            master,

            "Conflict_Count",

            "Average_Oil_Price",

            color="Conflict_Severity",

            hover="Country Name",

            title="Conflict vs Oil Price"

        ),

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Yearly Impact Trend
    # ============================================================

    yearly = (

        master

        .groupby("Year")

        .agg({

            "Conflict_Count":"sum",

            "Military_Spending":"mean",

            "Inflation_Rate":"mean",

            "Average_Oil_Price":"mean"

        })

        .reset_index()

    )

    import plotly.express as px

    fig = px.line(

        yearly,

        x="Year",

        y=[

            "Conflict_Count",

            "Military_Spending",

            "Inflation_Rate",

            "Average_Oil_Price"

        ],

        markers=True,

        title="Global Impact Trend"

    )

    fig.update_layout(

        template="plotly_dark",

        height=550

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # Top 10 Impact Ranking
    # ============================================================

    st.subheader("🏆 Top 10 Impact Ranking")

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



    # ============================================================
    # Country Summary
    # ============================================================

    st.subheader("🌍 Country Impact Summary")

    summary = impact.copy()

    summary = summary.sort_values(
        "Impact_Score",
        ascending=False
    )

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # Dataset Summary
    # ============================================================

    st.subheader("📅 Dataset Summary")

    c1, c2 = st.columns(2)

    with c1:

        st.info(f"""

### Coverage

🌍 Countries

**{master['Country Name'].nunique()}**

📅 Years

**{master['Year'].min()} - {master['Year'].max()}**

📊 Records

**{len(master):,}**

""")

    with c2:

        st.info(f"""

### Variables

⚔️ Conflict Count

🪖 Military Spending

📈 Inflation Rate

🛢 Average Oil Price

🔥 Average Intensity

""")

    st.divider()

    # ============================================================
    # Executive Insights
    # ============================================================

    st.subheader("📌 Executive Insights")

    highest = impact.iloc[0]

    lowest = impact.iloc[-1]

    st.success(f"""

## Global Impact Summary

🏆 Highest Impact Country

**{highest['Country Name']}**

Impact Score : **{highest['Impact_Score']:.3f}**

---

🌍 Lowest Impact Country

**{lowest['Country Name']}**

Impact Score : **{lowest['Impact_Score']:.3f}**

---

📊 Average Global Impact Score

**{impact['Impact_Score'].mean():.3f}**

---

⚔️ Total Conflicts

**{int(master['Conflict_Count'].sum()):,}**

---

🪖 Average Military Spending

**{master['Military_Spending'].mean():,.2f}**

---

📈 Average Inflation

**{master['Inflation_Rate'].mean():.2f}%**

---

🛢 Average Oil Price

**${master['Average_Oil_Price'].mean():.2f}**

""")

    st.divider()

    # ============================================================
    # Download Section
    # ============================================================

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

            label="⬇ Download Impact Score Dataset",

            data=impact.to_csv(index=False),

            file_name="country_impact_score.csv",

            mime="text/csv"

        )

    st.divider()

    # ============================================================
    # Footer
    # ============================================================

    st.markdown(
        """
---
## 🌍 Global Conflict & Economic Impact Dashboard

### Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Scikit-learn

### Data Sources

- UCDP/PRIO Armed Conflict Dataset
- SIPRI Military Expenditure
- World Bank Inflation Data
- Global Oil Price Dataset

**Designed as an end-to-end Data Analytics Portfolio Project**
"""
    )
