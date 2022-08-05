import streamlit as st
import leafmap.foliumap as leafmap


def app():
    st.title("Welcome to the Demo")

    st.markdown(
        """
    Please click on tabs on the sidebar to get started
    """
    )

    m = leafmap.Map(locate_control=True)
    m.add_basemap("ROADMAP")
    m.to_streamlit(height=700)