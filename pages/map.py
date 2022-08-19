import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import numpy as np
from shapely.geometry import mapping
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['text.color'] = 'white'
matplotlib.rcParams['axes.labelcolor'] = 'white'
matplotlib.rcParams['xtick.color'] = 'white'
matplotlib.rcParams['ytick.color'] = 'white'
matplotlib.rcParams['font.size'] = 8
    
def get_rgb(x, cmap, norm):
    color = np.array(cmap(norm((x))))[:3]
    color = 255 * color
    return list(color)

def listit(t):
    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t

@st.cache(allow_output_mutation=True)
def load_data(value):
    df = gpd.read_file("../data/SJ9000.geojson", driver="GeoJSON")
    df["lng"] = df.geometry.centroid.x
    df["lat"] = df.geometry.centroid.y
    listed_coords = [listit(mapping(g)["coordinates"]) for g in df.geometry]
    df = pd.DataFrame(df)
    df.geometry = listed_coords
    
    results = pd.read_csv("../data/full_dataset_outputs.csv")
    df = df.merge(results[['uprn','current-energy-efficiency']], on='uprn', how='left')
    df = df.dropna(axis=1)

    # Set colours
    if value in ['current-energy-efficiency']:
        min_val = 20
    else:
        min_val = df[value].min()
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=min_val, vmax=df[value].max())
    df["fill_color"] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, cmap, norm  

def insert_color_bar(cmap, norm, value):    # Insert colour bar
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)
    fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
                cax=ax, orientation='horizontal', label=value, aspect=3, extend='both')
    fig.set_facecolor('none')
    st.pyplot(fig)

def render_map(df):
    xMax, xMin = df.lng.max(), df.lng.min()
    yMax, yMin = df.lat.max(), df.lat.min()
    LAND_COVER = [[[xMin, yMin], [xMin, yMax], [xMax, yMax], [xMax, yMin]]]

    tooltip = {"html": "<b>Postcode:</b> {postcode} <br /><b>EPC:</b> {current-energy-efficiency}"}

    st.pydeck_chart(pdk.Deck(
            layers = [
                pdk.Layer(
                "PolygonLayer",
                df,
                id="geojson",
                opacity=0.8,
                stroked=False,
                get_polygon="geometry",
                filled=True,
                extruded=True,
                wireframe=True,
                get_elevation="AbsHMax*0.2",
                get_fill_color="fill_color",
                get_line_color="fill_color",
                auto_highlight=True,
                pickable=True,
            ),
                pdk.Layer(
                "PolygonLayer",
                LAND_COVER,
                stroked=False,
                # processes the data as a flat longitude-latitude pair
                get_polygon="-",
                get_fill_color=[255, 255, 255, 20],
                )
            ],
            initial_view_state= pdk.ViewState(
                    longitude=df.lng.mean(), 
                    latitude=df.lat.mean(), 
                    zoom=12, 
                    min_zoom=11, 
                    max_zoom=15, 
                    pitch=70.5, 
                    bearing=0,
            ),
            map_style=pdk.map_styles.DARK,
            tooltip=tooltip,
        ))
    
def app(value="current-energy-efficiency"):
    st.title("Map")

    st.markdown(
        """
    WMCA Tile Map
    """
    )

    df, cmap, norm = load_data(value)
    
    render_map(df)
    insert_color_bar(cmap, norm, value)

app()