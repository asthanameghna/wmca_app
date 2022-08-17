from email.policy import default
import streamlit as st
# import leafmap.foliumap as leafmap
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from pages import heatmap


def app(epc_data, sample_outputs, predicted):

    st.title("EPC Rating")

    epc_rating = [0,20,40,60,80,100]

    column1, column2, column3 = st.columns(3)

    with column1:
        choice_result = st.selectbox('Summary of', ('EPC Ratings', 'Solar PV', 'Heating Source'))
    
    with column2:
        st.write('You selected:', choice_result)

    with column3:
        st.subheader('Area Summary')
        st.write('Population Density: 3649 people/km2')
        st.write('Total Houses: 434,190')
        st.write('Land Area: 267.77 km2')

    column1, column2 = st.columns(2)

    property_types = {
        'Bunglow': 'property-type_Bunglow',
        'House': 'property-type_House',
        'Flat': 'property-type_Flat',
        'Maisonette': 'property-type_Maisonette',
        'Park Home': 'property-type_Park home',
    }

    local_authority = {
        'City of Bristol': 'local-authority_E06000023',
        'Windsor and Maidenhead': 'local-authority_E06000040',
        'Cannock Chase': 'local-authority_E07000192',
        'Lichfield': 'local-authority_E07000194',
        'South Staffordshire': 'local-authority_E07000196',
        'North Warwickshire': 'local-authority_E07000218',
        'Nuneaton and Bedworth': 'local-authority_E07000219',
        'Rugby': 'local-authority_E07000220',
        'Stratford-on-Avon': 'local-authority_E07000221',
        'Warwick': 'local-authority_E07000222',
        'Bromsgrove': 'local-authority_E07000234',
        'Birmingham': 'local-authority_E08000025',
        'Coventry': 'local-authority_E08000026',
        'Dudley': 'local-authority_E08000027',
        'Sandwell': 'local-authority_E08000028',
        'Solihull': 'local-authority_E08000029',
        'Walsall': 'local-authority_E08000030',
        'Wolverhampton': 'local-authority_E08000031',
        'Redbridge': 'local-authority_E09000026'
    }

    local_authority_tag = {
        'E06000023':'City of Bristol',
        'E06000040':'Windsor and Maidenhead',
        'E07000192':'Cannock Chase',
        'E07000194':'Lichfield',
        'E07000196':'South Staffordshire',
        'E07000218':'North Warwickshire',
        'E07000219':'Nuneaton and Bedworth',
        'E07000220':'Rugby',
        'E07000221':'Stratford-on-Avon',
        'E07000222':'Warwick',
        'E07000234':'Bromsgrove',
        'E08000025':'Birmingham',
        'E08000026':'Coventry',
        'E08000027':'Dudley',
        'E08000028':'Sandwell',
        'E08000029':'Solihull',
        'E08000030':'Walsall',
        'E08000031':'Wolverhampton',
        'E09000026':'Redbridge' 
    }

    groups = {
        # 'Property Type': 'property_types',
        'Postcode': 'postcode',
        'Current Energy Rating': 'current-energy-rating',
        'MSOA Code': 'msoa-code',
        'LSOA Code': 'lsoa-code',
        'Constituency': 'constituency',
        'Mean Consumption': 'mean-consumption',
        'Median Consumption': 'median-consumption',
        'Fuel Poverty': 'prop_household_fuel_poor'
        # 'Local Authority': 'local_authority'
    }    

    group_names = [key for key in groups.keys()]
    group_tag = [value for value in groups.values()]

    with column1:
        choice_group_x = st.selectbox('Group by X', (group_names))
        choice_group_y = st.selectbox('Group by Y', (group_names))
        st.write('You selected: ', choice_group_x, ' for X-axis and ', choice_group_y, ' for Y-axis')


    with column2:
        group = pd.DataFrame({'X value': epc_data[groups[choice_group_x]], 
                            'Y value': epc_data[groups[choice_group_y]]})
        st.bar_chart(group.groupby(['X value']).mean())

    # final = loc_auth_mean.drop(columns=['Unnamed: 0','uprn','mainheat-description','floor-height','total-floor-area','total_consumption','median_consumption','prop_households_fuel_poor','LATITUDE','LONGITUDE','prediction_confidence','predicted','additional_load'])

    loc_auth_epcdist = sample_outputs.groupby(['original-local-authority','current-energy-rating']).mean()
    loc_auth_eemean = sample_outputs.groupby(['original-local-authority'])['current-energy-efficiency'].mean()
    loc_auth_epc_count = pd.DataFrame(sample_outputs.groupby(['original-local-authority','current-energy-rating'])['uprn'].count())
    loc_auth_predpercent = predicted.groupby(['original-local-authority'])['predicted'].sum()/predicted.groupby(['original-local-authority'])['predicted'].count()*100

    loc_auth_epc = sample_outputs.groupby(['original-local-authority','current-energy-rating'])
    loc_auth_epc_dic = pd.DataFrame(sample_outputs.groupby(['original-local-authority','current-energy-rating'])).apply(list).to_dict()
    loc_auth = sample_outputs.groupby(['original-local-authority'])

    loc_auth_epc_rating = []
    for mean in loc_auth_eemean:
        if mean <= 20:
            loc_auth_epc_rating.append('G')
        elif mean <= 38:
            loc_auth_epc_rating.append('F')
        elif mean <= 54:
            loc_auth_epc_rating.append('E')
        elif mean <= 68:
            loc_auth_epc_rating.append('D')
        elif mean <= 80:
            loc_auth_epc_rating.append('C')
        elif mean <= 91:
            loc_auth_epc_rating.append('B')
        else:
            loc_auth_epc_rating.append('A')
    
    distributions = []

    
  
    #     dist = epc_count/loc_auth*100
    #     distributions.append(dist)
    # dont use group by just go for nested for / if

    # for key,value in local_authority_tag.items():
    #     st.write(key, ' : ', len(loc_auth.groups[key])) 
    #     if (key,'C') in loc_auth_epc_dic:
    #         st.write(len('C : ', loc_auth_epc.get_group((key,'C'))))

    

    final = pd.DataFrame(sample_outputs.groupby(['original-local-authority'])['uprn'].count())
    final['local-authority-name'] = ['City of Bristol','Windsor and Maidenhead','Cannock Chase','Lichfield','South Staffordshire','North Warwickshire','Nuneaton and Bedworth','Rugby','Stratford-on-Avon','Warwick','Bromsgrove','Birmingham','Coventry','Dudley','Sandwell','Solihull','Walsall','Wolverhampton','Redbridge']
    final['average-epc'] = loc_auth_eemean
    final['average-epc-rating'] = loc_auth_epc_rating
    #epc dist before this
    final['pred-percentage'] = loc_auth_predpercent



    # st.table(distributions)
    st.table(final)
    # st.table(loc_auth_epc_count)

    heatmap.app("current-energy-efficiency")
