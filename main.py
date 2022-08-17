import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from pages import home, map, heatmap, epc_rating, solar_pv, heating_type
from streamlit_option_menu import option_menu
import os

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

pathname = os.getcwd()  # your pathname

st.markdown(
    """
    <style>
    .main {
        background-color: F5F5F
    }
    </style>
    """,
    unsafe_allow_html = True
)

@st.cache
def get_data(filename):
    data = pd.read_csv(filename)
    return data

with header:
    st.title('WMCA - Pure LeapFrog Demo')
    st.text('')

with dataset:
    st.header('EPC data')
    epc_data = get_data(pathname+'data/numerical_individual_columns_data.csv')
    sample_outputs = get_data(pathname+'data/sample_outputs.csv')
    predicted = get_data(pathname+'data/sample_outputs_old.csv')
    st.dataframe(epc_data.head())
    st.header('Sample Outputs data')
    st.dataframe(sample_outputs.head())
    current_energy_rating = pd.DataFrame(epc_data['current-energy-rating'].value_counts())
    st.bar_chart(current_energy_rating)

    ####### plotly animation #####

    # epc_data['construction-age-band'] = pd.to_datetime(epc_data['construction-age-band']).dt.strftime('%Y-%m-%d')
    # construction_age_band = epc_data['construction-age-band'].unique().tolist()
    # fig1 = px.scatter(epc_data, x='constituency', y='mean_counsumption', animation_frame='construction-age-band')
    # st.write(fig1)  

######## maps ####
# st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

pages = [
        {"func": home.app, "title": "Home", "icon": "house"},
        {"func": epc_rating.app, "title": "EPC Rating", "icon": "bar-chart-line"},
        {"func": solar_pv.app, "title": "Solar PV", "icon": "brightness-high"},
        {"func": heating_type.app, "title": "Heating Type", "icon": "building"}
]


titles = [app["title"] for app in pages]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in pages]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )    


for app in pages:
    if app["title"] == selected:
        app["func"](epc_data, sample_outputs, predicted)
        break
    


# with features:
#     st.header('feature')


# with model_training:            
#     st.header('model')