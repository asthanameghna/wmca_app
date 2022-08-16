from distutils.command import config
import streamlit as st
# import leafmap.kepler as kepler
import geopandas as gpd


def app():
    st.title("Map")

    st.markdown(
        """
    WMCA Tile Map
    """
    )

    # shp_file_path = '/Users/meghna_mac2/PycharmProjects/WMCA/wmca_app/data/WMCA_shapefile/LAD_DEC_2021_GB_BFC.shp'
    # # shp_file = gpd.read_file(shp_file_path)
    # m = kepler.Map(center=[40, -100], zoom=2, height=600, widescreen=True)
    # m.add_shp(shp_file_path, "WMCA Tiles")
    # m.to_streamlit()