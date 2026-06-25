# ============================================================
# Data Loader
# ============================================================

import streamlit as st
import pandas as pd


# ============================================================
# Dashboard Dataset Loader
# ============================================================

@st.cache_data(show_spinner=False)
def load_dashboard_data():

    master = pd.read_csv(
        "dashboard_master.csv"
    )

    conflict = pd.read_csv(
        "dashboard_conflicts.csv"
    )

    economy = pd.read_csv(
        "dashboard_economy.csv"
    )

    impact = pd.read_csv(
        "dashboard_impact.csv"
    )

    yearly = pd.read_csv(
        "dashboard_yearly.csv"
    )

    kpi = pd.read_csv(
        "dashboard_kpi.csv"
    )

    return (
        master,
        conflict,
        economy,
        impact,
        yearly,
        kpi
    )


# ============================================================
# Country List
# ============================================================

def get_country_list(master):

    countries = sorted(
        master["Country Name"]
        .dropna()
        .unique()
    )

    return countries


# ============================================================
# Year Range
# ============================================================

def get_year_range(master):

    minimum = int(
        master["Year"].min()
    )

    maximum = int(
        master["Year"].max()
    )

    return minimum, maximum


# ============================================================
# Filter Data
# ============================================================

def filter_master_data(
    master,
    country,
    year_range
):

    data = master.copy()

    if country != "All Countries":

        data = data[
            data["Country Name"] == country
        ]

    data = data[

        (data["Year"] >= year_range[0]) &
        (data["Year"] <= year_range[1])

    ]

    return data


# ============================================================
# Dashboard KPIs
# ============================================================

def calculate_kpis(data):

    return {

        "Total Conflicts":

            int(
                data["Conflict_Count"].sum()
            ),

        "Countries":

            data["Country Name"].nunique(),

        "Average Military":

            round(
                data["Military_Spending"].mean(),
                2
            ),

        "Average Inflation":

            round(
                data["Inflation_Rate"].mean(),
                2
            ),

        "Average Oil":

            round(
                data["Average_Oil_Price"].mean(),
                2
            )

    }
