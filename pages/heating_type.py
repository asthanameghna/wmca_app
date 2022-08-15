import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt


def app(epc_data, sample_outputs, predicted):

    st.title("Heating Type")

    st.header('Target Electric Heating')

    column1, column2 = st.columns(2)

    with column1:
        percent = st.slider(
        'Percentage of homes to install electric heating',
        5.0, 100.0, 10.0)
        st.write('Target Percentage Selected:', percent)

    output = 3490
    num_house = 135000
    with column2:
        st.subheader('Impact')
        st.write('Total output: ', output, ' KWh')
        st.write('Houses with Electric Heating: ', num_house)
    

    st.header('House Heating Type')

    column1, column2 = st.columns(2)

    with column1:
        group = pd.DataFrame({'current-energy-rating': epc_data['current-energy-rating'], 
                            'total-floor-area': epc_data['total-floor-area']})
        labels = 'HeatingType1', 'HeatingType2', 'HeatingType3', 'HeatingType4'
        sizes = [15, 30, 45, 10]
        explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)
    
    with column2:
        st.subheader('Area Summary')
        st.write('Population Density: 3649 people/km2')
        st.write('Total Houses: 434,190')
        st.write('Land Area: 267.77 km2')
 
      

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
