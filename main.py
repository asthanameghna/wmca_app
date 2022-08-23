import streamlit as st
import pandas as pd
from pages import render_map
import geopandas as gpd
from shapely.geometry import mapping
import matplotlib
import numpy as np
import pickle

st. set_page_config(layout="wide")

@st.cache
def get_data(filename):
    data = pd.read_csv(filename)
    return data

def listit(t):
    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t

def get_rgb(x, cmap, norm):
    color = np.array(cmap(norm((x))))[:3]
    color = 255 * color
    return list(color)

@st.cache
def EPC_map_data():
    PATH = "C:/Users/lilia/Documents/GitHub/WMCA/DSSG_WMCA/data/processed/output/SJ9000.geojson"
    df = gpd.read_file(PATH, driver="GeoJSON")
    df["lng"] = df.geometry.centroid.x
    df["lat"] = df.geometry.centroid.y
    listed_coords = [listit(mapping(g)["coordinates"]) for g in df.geometry]
    df = pd.DataFrame(df)
    df.geometry = listed_coords
    
    results = pd.read_csv("data/full_dataset_outputs.csv")
    df = df[['lat','lng','geometry', 'postcode','uprn']].merge(results[['uprn','current-energy-efficiency']], on='uprn', how='left')
    df = df.dropna()
    
    value = 'current-energy-efficiency'
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=20, vmax=100)
    
    df['fill_color'] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, norm

@st.cache
def pv_map_data():
    PATH = "data\\building_pv.geojson"
    df = gpd.read_file(PATH, driver="GeoJSON")
    df["lng"] = df.geometry.centroid.x
    df["lat"] = df.geometry.centroid.y
    listed_coords = [listit(mapping(g)["coordinates"]) for g in df.geometry]
    df = pd.DataFrame(df)[['lat', 'lng', 'geometry', 'pv_output']]
    df.geometry = listed_coords
    
    value = 'pv_output'
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=df['pv_output'].quantile(0.05), vmax=df['pv_output'].quantile(0.95))
    
    df['fill_color'] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, norm

@st.cache
def load_data(path, extension):
    if extension == "csv":
        df = pd.read_csv(path)
    elif extension == 'geojson':
        df = gpd.read_file(path, driver="GeoJSON")
    return df

with open('data/dictionaries/groups.pickle', 'rb') as handle:
    groups = pickle.load(handle)
group_names = [key for key in groups.keys()]
group_tag = [value for value in groups.values()]

with open('data/dictionaries/local_authority.pickle', 'rb') as handle:
    local_authority = pickle.load(handle)

with open('data/dictionaries/property_types.pickle', 'rb') as handle:
    property_types = pickle.load(handle)

with open('data/dictionaries/local_authority_tag.pickle', 'rb') as handle:
    local_authority_tag = pickle.load(handle)

tab1, tab2, tab3 = st.tabs(['EPC Rating 🏠', "Solar PV ☀️", "Heating Type ⚡️"])

with tab1:
    st.header("EPC Rating 🏠")
    epc_data = load_data("data\\full_dataset_outputs.csv", 'csv')
    column1, column2, column3 = st.columns([2,1,1])

    with column1:
        epc_df, epc_norm = EPC_map_data()
        render_map.app(epc_df, epc_norm)

    with column2:
        st.subheader('Area Summary')
        st.write('Population Density: 3649 people/km2')
        st.write('Total Houses: 434,190')
        st.write('Land Area: 267.77 km2')    

    with column3:
        choice_group_x = st.selectbox('Group by X', (group_names))
        choice_group_y = st.selectbox('Group by Y', (group_names))
        st.write('You selected: ', choice_group_x, ' for X-axis and ', choice_group_y, ' for Y-axis')
        
        group = pd.DataFrame({'X value': epc_data[groups[choice_group_x]], 
                            'Y value': epc_data[groups[choice_group_y]]})
        st.bar_chart(group.groupby(['X value']).mean())

with tab2:
    st.header("Solar PV ☀️")
    solar_data = load_data("data\\building_pv.geojson", 'geojson')
    column1, column2, column3 = st.columns([2,1,1])

    with column1:
        pv_df, pv_norm = pv_map_data()
        render_map.app(pv_df, pv_norm)

    with column2:
        st.subheader('Area Summary')
        st.write('Population Density: 3649 people/km2')
        st.write('Total Houses: 434,190')
        st.write('Land Area: 267.77 km2')  

    with column3:
        st.subheader("NA")

with tab3:
    st.header("Heating Type ⚡️")