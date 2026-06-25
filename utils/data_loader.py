import pandas as pd
import streamlit as st

@st.cache_data
def load_dashboard_data():

    master = pd.read_csv(
        "Data_Processed/global_conflict_master_dataset.csv"
    )

    conflict = pd.read_csv(
        "Data_Processed/clean_conflict.csv"
    )

    military = pd.read_csv(
        "Data_Processed/clean_military.csv"
    )

    inflation = pd.read_csv(
        "Data_Processed/clean_inflation.csv"
    )

    oil = pd.read_csv(
        "Data_Processed/clean_oil.csv"
    )

    return (
        master,
        conflict,
        military,
        inflation,
        oil
    )
