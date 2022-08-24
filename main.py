import streamlit as st
import pandas as pd
from pages import render_map, about
import geopandas as gpd
from shapely.geometry import mapping
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
import plotly.figure_factory as ff
import plotly.express as px

st. set_page_config(layout="wide")

# Set sidebar
about.app()

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
    df = pd.DataFrame(df)[['lat', 'lng', 'geometry', 'pv_output','shading_mean', 'calculatedAreaValue', 'AbsHMax']]
    df.geometry = listed_coords
    
    value = 'pv_output'
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=df[value].quantile(0.05), vmax=df[value].quantile(0.95))
    
    df['fill_color'] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, norm

@st.cache
def heating_map_data(df):
    listed_coords = [listit(mapping(g)["coordinates"]) for g in df.geometry]
    df = pd.DataFrame(df)[['lat', 'lng', 'geometry', 'additional_peak_load', 'predicted', 'AbsHMax']]
    df.geometry = listed_coords
    
    value = 'additional_peak_load'
    cmap = matplotlib.cm.get_cmap('RdYlGn')
    norm = matplotlib.colors.Normalize(vmin=df[value].quantile(0.05), vmax=df[value].quantile(0.95))
    
    df['fill_color'] = df[value].apply(lambda row: get_rgb(row, cmap, norm))

    return df, norm

def load_data(path):
    df = gpd.read_file(path, driver="GeoJSON")
    return df

@st.cache
def get_data(filename):
    data = pd.read_csv(filename)
    return data

local_authority_ = {
        'City of Bristol': 'E06000023',
        'Windsor and Maidenhead': 'E06000040',
        'Cannock Chase': 'E07000192',
        'Lichfield': 'E07000194',
        'South Staffordshire': 'E07000196',
        'North Warwickshire': 'E07000218',
        'Nuneaton and Bedworth': 'E07000219',
        'Rugby': 'E07000220',
        'Stratford-on-Avon': 'E07000221',
        'Warwick': 'E07000222',
        'Bromsgrove': 'E07000234',
        'Birmingham': 'E08000025',
        'Coventry': 'E08000026',
        'Dudley': 'E08000027',
        'Sandwell': 'E08000028',
        'Solihull': 'E08000029',
        'Walsall': 'E08000030',
        'Wolverhampton': 'E08000031',
        'Redbridge': 'E09000026'
    }

def get_max_energy_output(loc_auth):
        new_df = sample_outputs[sample_outputs['original-local-authority'] == (local_authority_[loc_auth])]
        en_out = np.ceil(np.mean(new_df['total_consumption'])).astype(int)
        return en_out

def get_add_load_output(loc_auth):
        new_df = sample_outputs[sample_outputs['original-local-authority'] == (local_authority_[loc_auth])]
        en_out = np.ceil(np.mean(new_df['additional_load'])).astype(int)
        return en_out

def get_elec_heat_per(loc_auth):
        new_df = sample_outputs[sample_outputs['original-local-authority'] == (local_authority_[loc_auth])]
        total_houses = len(new_df['uprn'])
        num_predicted_1 = len(new_df[new_df['predicted'] == 1])
        elec_heat_per = np.ceil(num_predicted_1/total_houses*100).astype(int)
        return elec_heat_per

def get_solar_pv_output(loc_auth):
        new_df = sample_outputs[sample_outputs['original-local-authority'] == (local_authority_[loc_auth])]
        en_out = np.ceil(np.mean(new_df['total_consumption']))
        return en_out

# Load all data
data = load_data("data/data.geojson")

pathname = './'  # your pathname  

epc_data = get_data(pathname+'data/numerical_individual_columns_data_demo.csv')
sample_outputs = get_data(pathname+'data/sample_outputs_demo.csv')
predicted = get_data(pathname+'data/sample_outputs_old_demo.csv')
sj9000 = get_data(pathname+'data/SJ9000_results.csv')

with open('data/dictionaries/groups.pickle', 'rb') as handle:
    groups = pickle.load(handle)
group_names = [key for key in groups.keys()]
group_tag = [value for value in groups.values()]

with open('data/dictionaries/local_authority.pickle', 'rb') as handle:
    local_authority = pickle.load(handle)

with open('data/dictionaries/property_types.pickle', 'rb') as handle:
    property_types = pickle.load(handle)

with open('data/dictionaries/local_authority_tag.pickle', 'rb') as handle:
    local_authority_tag = pickle.load(handle)

tab1, tab2, tab3 = st.tabs(['EPC Rating 🏠', "Solar PV ☀️", "Heating Type ⚡️"])

with tab1:
    st.header("EPC Rating 🏠")
    st.markdown("""
    Only 40\% of the houses in the West Midlands have an Energy Performance Certificate (EPC). We predicted the remaining 60\% using a random forest and similarity quantification model (which matches houses based on similar features) with a 55.47\% accuracy. We used building height, floor area, energy consumption and location-based data as our input values. Our accuracy was severely limited by the computational power we had available.
    
    """)
    column1, column2= st.columns([2,1])

    with column1:
        epc_df, epc_norm = EPC_map_data(data)
        render_map.app(epc_df, epc_norm, 'Current Energy Efficiency (%)')

    with column2:
        st.subheader('Area Summary')

        st.write(f'🏠Total Houses: {len(data)}')
        st.write(f'⭐️ Average EPC: {round(data["current-energy-efficiency"].mean(),2)}')  
        st.write(f'❓Predicted EPC ratings: {round(data["predicted"].sum()/len(data)*100,2)}%')  

        st.subheader('Prediction Summary')
        labels = ['Predicted', 'True']
        sizes = [data['predicted'].sum(), len(data)-data['predicted'].sum()]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title("Predicted vs True ratings")
        fig1.set_facecolor('none')
        st.pyplot(fig1)

    st.subheader('Choose a Plot for Visualisation')
    column1, column2= st.columns([1,1])
   
    with column1:
        choice_group_x = st.selectbox('Group by X', (group_names))

    with column2:
        choice_group_y = st.selectbox('Group by Y', (group_names))
                
    
    st.write('You selected: ', choice_group_x, ' for X-axis and ', choice_group_y, ' for Y-axis') 

    current_energy_rating = pd.DataFrame(data['current-energy-rating'].value_counts())
    st.bar_chart(current_energy_rating)     
        
    group = pd.DataFrame({'X value': data[groups[choice_group_x]], 
                            'Y value': data[groups[choice_group_y]]})
    # st.bar_chart(group.groupby(['X value']).mean())

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
    final['average-epc'] = loc_auth_eemean.astype(int)
    final['average-epc-rating'] = loc_auth_epc_rating
    #epc dist before this
    final['pred-percentage'] = loc_auth_predpercent.astype(int)



    # st.table(distributions)
    st.table(final)

with tab2:
    st.header("Solar PV ☀️")
    st.markdown("""
    We estimated the annual solar PV output for houses in the West Midlands using the calculations from [pvlib](https://pvlib-python.readthedocs.io/en/stable/index.html) which are within the same order of magnitude as estimates given by the Microgeneration Certification Scheme (MCS). The advantage of our method is that it does not require a site visit to get the roof slope, aspect, area and shading factor. However, due to technical issues on our secure platform, we were unable to run the calculations on all tiles. The results below represent 5km by 5km tile in Wolverhampton using pvlib.
    """)
    column1, column2 = st.columns([2,1])

    with column1:
        pv_df, pv_norm = pv_map_data(data)
        render_map.app(pv_df, pv_norm, 'Current Solar PV Output (kWhr/year)')

    with column2:
        st.subheader('Area Summary')
        st.write(f'🏠Total Houses: {len(data)}')
        st.write(f'☀️ Average solar pv output: {round(data["pv_output"].mean(),2)} kWhr/year')  
        st.write(f'🔆 Median solar pv output: {round(data["pv_output"].median(),2)}kWhr/year') 

        st.subheader('Prediction Summary')
        group = pd.DataFrame({'current-energy-rating': epc_data['current-energy-rating'], 
                            'total-floor-area': epc_data['total-floor-area']})
        labels = ['Solar Panel Installed Houses', 'Non-Solar Panel Installed Homes']
        num_predicted_0 = len(sample_outputs[sample_outputs['predicted'] == 0])
        num_predicted_1 = len(sample_outputs[sample_outputs['predicted'] == 1])
        per_predicted_0 = num_predicted_0/(num_predicted_0+num_predicted_1)
        per_predicted_1 = num_predicted_1/(num_predicted_0+num_predicted_1)
        sizes = [per_predicted_1, per_predicted_0]
        explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title("Predicted vs True Solar Installation")
        fig1.set_facecolor('none')
        st.pyplot(fig1)

    st.subheader('Target Solar Panel Installation')

    column1, column2 = st.columns([2,1])

    with column1:
        percent = st.slider(
        'Percentage of homes to install solar panels',
        30.0, 100.0, 40.0, step=10.0)
        st.write('Target Percentage Selected:', percent)

    num_house = len(sj9000['uprn'])
    per_house = np.around(num_house*percent/100).astype(int)
    per_output = np.ceil((np.mean(sj9000['pv_output'])/1000)*per_house).astype(int)
    
    with column2:
        st.subheader('Impact')
        st.write('Total output: ', per_output, ' MWh')
        st.write('Houses with Solar: ', per_house)


with tab3:
    st.header("Heating Type ⚡️")
    st.markdown("""
    We estimate the additional peak load and additional yearly load that will be put onto the electricity network if a home switches to a heat pump from a non-electric heating source. We first predicted the heating source using a random forest model with building height, floor area, energy consumption and location-based data as our input values. We extrapolated the additional energy consumption for homes of similar types from the EPC database to provide the additional yearly load that would be put onto the electricity network. Then, we used the national electricity demand with the yearly additional load value to determine the additional peak load for each home. This data can then be aggregated by substation distribution area so that the demand headroom for these stations can be compared to the additional load. This will determine if the substations need to be upgraded to handle the additional load.
    """)
    column1, column2 = st.columns([2,1])

    with column1:
        heating_df, heating_norm = heating_map_data(data)
        render_map.app(heating_df, heating_norm, 'Current Electric Heating Load (kWhr)')

    with column2:
        st.subheader('Area Summary')
        st.write(f'🏠Total Houses: {len(data)}')
        st.write(f'⚡️Average additional load: {round(data["additional_peak_load"].mean(),2)} kWhr')  
        st.write(f'❓Predicted heating types: {round(data["predicted"].sum()/len(data)*100,2)}%') 

        st.subheader('Prediction Summary')
        group = pd.DataFrame({'current-energy-rating': epc_data['current-energy-rating'], 
                            'total-floor-area': epc_data['total-floor-area']})
        labels = ['Electric Heating', 'Non-Electric Heating']
        num_predicted_0 = len(sample_outputs[sample_outputs['predicted'] == 0])
        num_predicted_1 = len(sample_outputs[sample_outputs['predicted'] == 1])
        per_predicted_0 = num_predicted_0/(num_predicted_0+num_predicted_1)
        per_predicted_1 = num_predicted_1/(num_predicted_0+num_predicted_1)
        sizes = [per_predicted_1, per_predicted_0]
        explode = (0, 0) 

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax1.set_title("Predicted vs True Electric Heating Type")
        fig1.set_facecolor('none')
        st.pyplot(fig1)
    
    column1, column2 = st.columns([2,1])

    with column1:
        st.subheader('Target Electric Heating')
        percent = st.slider(
        'Percentage of homes to install electric heating',
        30.0, 100.0, 40.0, step=10.0)
        st.write('Target Percentage Selected:', percent)

        num_house = len(sample_outputs['uprn'])
        per_house = np.around(num_house*percent/100).astype(int)
        per_output = np.ceil((np.mean(sample_outputs['additional_load'])/1000)*per_house).astype(int)

    with column2:
        st.subheader('Impact')
        st.write('Total output: ', per_output, ' MWh')
        st.write('Houses with Electric Heating: ', per_house)




    final = pd.DataFrame(sample_outputs.groupby(['original-local-authority'])['uprn'].count())
    final['local-authority-name'] = ['City of Bristol','Windsor and Maidenhead','Cannock Chase','Lichfield','South Staffordshire','North Warwickshire','Nuneaton and Bedworth','Rugby','Stratford-on-Avon','Warwick','Bromsgrove','Birmingham','Coventry','Dudley','Sandwell','Solihull','Walsall','Wolverhampton','Redbridge']

    max_energy_output = []
    add_load = []
    elec_heat_per = []
    for loc in final['local-authority-name']:
        max_energy_output.append(get_max_energy_output(loc)/1000)
        add_load.append(get_add_load_output(loc))
        elec_heat_per.append(get_elec_heat_per(loc))

    final['max-energy-output-MWh'] = max_energy_output
    final['additional-load-kWh'] = add_load
    final['electric-heating-percent'] = elec_heat_per

    
    st.table(final)

