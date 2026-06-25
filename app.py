# ============================================================
# Global Conflict & Economic Impact Dashboard
# Main Application
# ============================================================

import streamlit as st

from utils.data_loader import load_dashboard_data

from dashboard.executive_dashboard import show_executive_dashboard
from dashboard.conflict_dashboard import show_conflict_dashboard
from dashboard.military_dashboard import show_military_dashboard
from dashboard.inflation_dashboard import show_inflation_dashboard
from dashboard.oil_dashboard import show_oil_dashboard
from dashboard.impact_dashboard import show_impact_dashboard


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Global Conflict & Economic Impact Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.main{
    background-color:#0E1117;
}

.block-container{
    padding-top:1rem;
}

[data-testid="stSidebar"]{
    background-color:#161A28;
}

h1,h2,h3,h4,h5{
    color:white;
}

.metric-card{
    background:#1E1E1E;
    border-radius:10px;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# Load Data
# ============================================================

master, conflict, economy, impact, yearly, kpi = load_dashboard_data()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.image(
    "assets/logo.png",
    use_container_width=True
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(

    "",

    [

        "🏠 Executive Dashboard",

        "⚔️ Conflict Analysis",

        "🪖 Military Spending",

        "📈 Inflation Analysis",

        "🛢 Oil Price Analysis",

        "🌍 Global Impact"

    ]

)

st.sidebar.markdown("---")

# ============================================================
# Global Filters
# ============================================================

countries = sorted(
    master["Country Name"].dropna().unique()
)

country = st.sidebar.selectbox(

    "Country",

    ["All Countries"] + countries

)

year_min = int(master["Year"].min())

year_max = int(master["Year"].max())

year_range = st.sidebar.slider(

    "Year",

    year_min,

    year_max,

    (year_min, year_max)

)

filtered = master.copy()

if country != "All Countries":

    filtered = filtered[
        filtered["Country Name"] == country
    ]

filtered = filtered[

    (filtered["Year"] >= year_range[0]) &
    (filtered["Year"] <= year_range[1])

]

# ============================================================
# Navigation
# ============================================================

if page == "🏠 Executive Dashboard":

    show_executive_dashboard(
        filtered,
        impact
    )

elif page == "⚔️ Conflict Analysis":

    show_conflict_dashboard(
        filtered
    )

elif page == "🪖 Military Spending":

    show_military_dashboard(
        filtered
    )

elif page == "📈 Inflation Analysis":

    show_inflation_dashboard(
        filtered
    )

elif page == "🛢 Oil Price Analysis":

    show_oil_dashboard(
        filtered
    )

elif page == "🌍 Global Impact":

    show_impact_dashboard(
        filtered
    )

# ============================================================
# Footer
# ============================================================

st.sidebar.markdown("---")

st.sidebar.success(
    "Global Conflict & Economic Impact Dashboard"
)

st.sidebar.caption(
    "Developed using Python, Pandas, Plotly & Streamlit"
)


