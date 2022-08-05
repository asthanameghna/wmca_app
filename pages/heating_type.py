import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd


def app():

    st.title("Heating Type")
    

    epc_data = pd.read_csv("/Users/meghna_mac2/PycharmProjects/WMCA/wmca_app/data/numerical_individual_columns_data.csv")
    epc_rating = [0,20,40,60,80,100]

    column1, column2 = st.columns(2)
    
    
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

      
    choice_result = st.selectbox('Summary of', ('EPC Ratings', 'Solar PV', 'Heating Source'))
    
    st.write('You selected:', choice_result)

    st.write('Area Summary')
    st.write('Population Density: 3649 people/km2')
    st.write('Total Houses: 434,190')
    st.write('Land Area: 267.77 km2')

    choice_group = st.selectbox('Group by', ('Floor Area', 'House Type', 'Wall Type', 'Height'))
    st.write('You selected:', choice_group)

    if choice_group=='Floor Area':
        choice_group = 'total-floor-area'
    elif choice_group=='House Type':
        choice_group = 'property-type'  
    elif choice_group=='House Type':
        choice_group = 'property-type' 
    elif choice_group=='Wall Type':
        choice_group = 'wall-type'   
    else:
        choice_group = 'floor-height' 

    group = pd.DataFrame({'current-energy-rating': epc_data['current-energy-rating'], 
                            'total-floor-area': epc_data['total-floor-area']})
    st.bar_chart(group.groupby(['current-energy-rating']).mean())
