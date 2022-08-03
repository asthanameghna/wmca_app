import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd


def app():

    st.title("Heatmap")
    

    epc_data = pd.read_csv("/Users/meghna_mac2/PycharmProjects/WMCA/wmca_app/data/numerical_individual_columns_data.csv")
    epc_rating = [0,20,40,60,80,100]

    m = leafmap.Map(tiles="stamentoner")
    m.add_heatmap(
        epc_data,
        latitude="LATITUDE",
        longitude="LONGITUDE",
        value="current-energy-efficiency",
        name="Heat map",
        radius=20,
    )
    # m.add_legend(epc_data, title='Legend')
    m.to_streamlit(height=700)