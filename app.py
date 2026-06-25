import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from utils.data_loader import load_dashboard_data

from dashboard.executive_dashboard import show_executive_dashboard
from dashboard.conflict_dashboard import show_conflict_dashboard
from dashboard.military_dashboard import show_military_dashboard
from dashboard.inflation_dashboard import show_inflation_dashboard
from dashboard.oil_dashboard import show_oil_dashboard
from dashboard.impact_dashboard import show_impact_dashboard
from dashboard.world_map_dashboard import show_world_map_dashboard


# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Global Conflict & Economic Impact Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

master, conflict, military, inflation, oil = load_dashboard_data()

# -------------------------------------------------------
# Create Impact Dataset
# -------------------------------------------------------

impact = (
    master
    .groupby("Country Name")
    .agg({
        "Conflict_Count": "sum",
        "Average_Intensity": "mean",
        "Military_Spending": "mean",
        "Inflation_Rate": "mean",
        "Average_Oil_Price": "mean"
    })
    .reset_index()
)

scaler = MinMaxScaler()

cols = [
    "Conflict_Count",
    "Average_Intensity",
    "Military_Spending",
    "Inflation_Rate",
    "Average_Oil_Price"
]

impact[cols] = scaler.fit_transform(impact[cols])

impact["Impact_Score"] = (
      0.35 * impact["Conflict_Count"]
    + 0.25 * impact["Average_Intensity"]
    + 0.20 * impact["Military_Spending"]
    + 0.10 * impact["Inflation_Rate"]
    + 0.10 * impact["Average_Oil_Price"]
)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("🌍 Navigation")

page = st.sidebar.radio(

    "Select Dashboard",

    [

        "🏠 Executive Dashboard",

        "⚔️ Conflict Dashboard",

        "🪖 Military Dashboard",

        "📈 Inflation Dashboard",

        "🛢 Oil Dashboard",

        "🌍 Global Impact Dashboard",

        "🗺️ World Map Dashboard"

    ]

)

# -------------------------------------------------------
# Navigation
# -------------------------------------------------------

if page == "🏠 Executive Dashboard":

    show_executive_dashboard(master, impact)

elif page == "⚔️ Conflict Dashboard":

    show_conflict_dashboard(master)

elif page == "🪖 Military Dashboard":

    show_military_dashboard(master)

elif page == "📈 Inflation Dashboard":

    show_inflation_dashboard(master)

elif page == "🛢 Oil Dashboard":

    show_oil_dashboard(master)

elif page == "🌍 Global Impact Dashboard":

    show_impact_dashboard(master)

elif page == "🗺️ World Map Dashboard":

    show_world_map_dashboard(master)

