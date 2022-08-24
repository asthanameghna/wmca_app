import streamlit as st
import pandas as pd
from pages import render_map
import geopandas as gpd
from shapely.geometry import mapping
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json

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
def EPC_map_data(df):
    listed_coords = [listit(mapping(g)["coordinates"]) for g in df.geometry]
    df = pd.DataFrame(df)
    df.geometry = listed_coords
    
    # Only keep cols for energy efficiency
    df = df[['lat','lng','geometry', 'postcode','uprn', 'current-energy-efficiency', 'AbsHMax']]
    
    value = 'current-energy-efficiency'
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=20, vmax=100)
    
    df['fill_color'] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, norm

@st.cache
def pv_map_data(df):
    listed_coords = [listit(mapping(g)["coordinates"]) for g in df.geometry]
    df = pd.DataFrame(df)[['lat', 'lng', 'geometry', 'postcode', 'pv_output','shading_mean', 'calculatedAreaValue', 'AbsHMax']]
    df.geometry = listed_coords
    
    value = 'pv_output'
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=df[value].quantile(0.05), vmax=df[value].quantile(0.95))
    
    df['fill_color'] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, norm

@st.cache
def heating_map_data(df):
    listed_coords = [listit(mapping(g)["coordinates"]) for g in df.geometry]
    df = pd.DataFrame(df)[['lat', 'lng', 'geometry', 'postcode', 'additional_peak_load', 'predicted', 'AbsHMax']]
    df.geometry = listed_coords
    
    value = 'additional_peak_load'
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=df[value].quantile(0.05), vmax=df[value].quantile(0.95))
    
    df['fill_color'] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, norm

def load_data(path):
    df = gpd.read_file(path, driver="GeoJSON")
    return df

# Load all data
data = load_data("data/data.geojson")

with open('data/dictionaries/groups.json', 'rb') as handle:
    groups = json.load(handle)
group_names = [key for key in groups.keys()]
group_tag = [value for value in groups.values()]

with open('data/dictionaries/local_authority.json', 'rb') as handle:
    local_authority = json.load(handle)

with open('data/dictionaries/property_types.json', 'rb') as handle:
    property_types = json.load(handle)

with open('data/dictionaries/local_authority_tag.json', 'rb') as handle:
    local_authority_tag = json.load(handle)

tab1, tab2, tab3 = st.tabs(['EPC Rating 🏠', "Solar PV ☀️", "Heating Type ⚡️"])

with tab1:
    st.header("EPC Rating 🏠")
    column1, column2 = st.columns([2,2])

    with column1:
        epc_df, epc_norm = EPC_map_data(data)
        render_map.app(epc_df, epc_norm,'Energy Efficiency')

    with column2:
        st.subheader('Area Summary')
        st.write(f'🏠Total Houses: {len(data)}')
        st.write(f'⭐️ Average EPC: {round(data["current-energy-efficiency"].mean(),2)}')  
        st.write(f'❓Predicted EPC ratings: {round(data["predicted"].sum()/len(data)*100,2)}%')

        # labels = ['Predicted', 'True']
        # sizes = [data['predicted'].sum(), len(data)-data['predicted'].sum()]

        # fig1, ax1 = plt.subplots()
        # ax1.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90)
        # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # ax1.set_title("Predicted vs True ratings")
        # fig1.set_facecolor('none')
        # st.pyplot(fig1)
        st.subheader('Distribution of energy efficiency')
        current_energy_rating = pd.DataFrame(data['current-energy-rating'].value_counts())
        st.bar_chart(current_energy_rating)

    st.subheader('Explore the data')

    column1, column2 = st.columns([1,2])
    with column1:
        choice_group_x = st.selectbox('Group by X', (group_names))
        choice_group_y = st.selectbox('Group by Y', (group_names))
        st.write('You selected: ', choice_group_x, ' for X-axis and ', choice_group_y, ' for Y-axis')  
      
    with column2:
        group = pd.DataFrame({
            'X value': data[groups[choice_group_x]], 
            'Y value': data[groups[choice_group_y]]
            })
        st.bar_chart(group.groupby(['X value']).mean())

with tab2:
    st.header("Solar PV ☀️")
    column1, column2 = st.columns([2,2])

    with column1:
        pv_df, pv_norm = pv_map_data(data)
        render_map.app(pv_df, pv_norm,'Solar PV Output (kWhr/year')

    with column2:
        st.subheader('Area Summary')
        st.write(f'🏠Total Houses: {len(data)}')
        st.write(f'☀️ Average solar pv output: {round(data["pv_output"].mean(),2)}')  
        st.write(f'🔆 Median solar pv output: {round(data["pv_output"].median(),2)}')  

        pv_output = pd.DataFrame(data['pv_output'].value_counts())
        st.bar_chart(pv_output)

with tab3:
    st.header("Heating Type ⚡️")
    column1, column2, column3 = st.columns([2,1,1])

    with column1:
        heating_df, heating_norm = heating_map_data(data)
        render_map.app(heating_df, heating_norm, 'Additional peak load (kWhr)')

    with column2:
        st.subheader('Area Summary')
        st.write(f'🏠Total Houses: {len(data)}')
        st.write(f'⚡️Average additional load: {round(data["additional_peak_load"].mean(),2)}')  
        st.write(f'❓Predicted heating types: {round(data["predicted"].sum()/len(data)*100,2)}%')

        additional_peak_load = pd.DataFrame(data['additional_peak_load'].value_counts())
        st.bar_chart(pv_output)
