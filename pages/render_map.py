import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['text.color'] = 'white'
matplotlib.rcParams['axes.labelcolor'] = 'white'
matplotlib.rcParams['xtick.color'] = 'white'
matplotlib.rcParams['ytick.color'] = 'white'
matplotlib.rcParams['font.size'] = 8

def insert_color_bar(norm, value):    # Insert colour bar
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
                cax=ax, orientation='horizontal', label=value, aspect=3, extend='both')
    fig.set_facecolor('none')
    st.pyplot(fig)

def plot_map(df):
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
                    zoom=13, 
                    min_zoom=11, 
                    max_zoom=15, 
                    pitch=70.5, 
                    bearing=0,
            ),
            map_style=pdk.map_styles.DARK,
            tooltip=tooltip,
        ))
    
def app(df, norm, value):    
    plot_map(df)
    insert_color_bar(norm, value)

