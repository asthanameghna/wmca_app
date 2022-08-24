import streamlit as st

def app():
    st.markdown(
    """
    <style>
    .sidebar .sidebar-cosntent {
        background-color: black;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.subheader('About')
        st.markdown("""
        In the summer of 2022, we worked with WMCA and Pure Leapfrog to help strategise reducing carbon emissions and non-renewable energy usage from homes. We used licensed and open-source data to: 
        
        1. Predict the energy efficiency of 1.2 million homes
        2. Estimate yearly solar PV output 
        3. Predict whether homes had electric or non-electric heating
        4. Determine the impact of switching to electric heating on the power grid.
        [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/DSSGxUK/s22_wmca) 
        """, unsafe_allow_html=True)

        st.subheader("Contributors")
        st.markdown("""
        [![Repo](https://badgen.net/badge/Ang%20Li-Lian/LinkedIn/blue)](https://www.linkedin.com/in/anglilian/) 
        [![Repo](https://badgen.net/badge/Meghna%20Asthana/LinkedIn/blue)](https://www.linkedin.com/in/meghna-asthana-1452b097/) 
        [![Repo](https://badgen.net/badge/Mike%20Coughlan/LinkedIn/blue)](https://www.linkedin.com/in/mike-k-coughlan/) 
        [![Repo](https://badgen.net/badge/Shriya%20Kamat%20Tarcar/LinkedIn/blue)](https://www.linkedin.com/in/shriya-c-k-tarcar-6083641bb/) 
                
        """, unsafe_allow_html=True)

        st.subheader("Partners")
        st.image("images/DSSGxUK_logo.png")
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.image("images/West_Midlands_Combined_Authority_logo.svg.png")
        with col2:
            st.image("images/pure_leapfrog_logo.png")
        with col3:
            st.image("images/WarwickLogo.png")
