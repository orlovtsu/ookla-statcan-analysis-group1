# Importing relevant packages
import streamlit as st
import folium
from streamlit_folium import folium_static
from matplotlib import cm
import pandas as pd
import sys

# changing system path
sys.path.append("/home/ubuntu/ookla-statcan-analysis-group1/scripts/data")

# changing layout of streamlit app
st.set_page_config(layout="wide")

# ignoring depracation warning from st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# importing my data processing module
import process_data



# ------------------- Streamlit App ------------------------

# title of streanlit app
st.title("Ookla StatCan Analysis - Group 1")

st.write("""
In this Streamlit App, we analyse Internet download speeds across canada using the 'Ookla-StatCan data,and try to figure out what factors affect speeds across provinces, the impacts of connection type of internet speeds, and the correlation with Median income.
""")


# calling data from imported module
@st.cache_data
def income_pct():
    return process_data.income_pct()

# loading the processed statcan data from 'process_data' module
df_1 = income_pct()

# list of provinces in Canada
province = ['Alberta',
                'Newfoundland and Labrador / Terre-Neuve-et-Labrador',
                'Prince Edward Island / Île-du-Prince-Édouard',
                'Nova Scotia / Nouvelle-Écosse',
                'New Brunswick / Nouveau-Brunswick',
                'Quebec / Québec',
                'Ontario',
                'Manitoba',
                'Saskatchewan',
                'British Columbia / Colombie-Britannique',
                'Northwest Territories / Territoires du Nord-Ouest',
                'Nunavut',
                'Yukon']


# selectbox for selecting province to filter data by
province_1 = st.selectbox('Select a Province', province)

# subheader of first visualization
st.subheader(f'#1. How many towns "{province_1}" met the 50/10 target?')

#1. provincial targets
@st.cache_resource
def plot_target(province):
    df = df_1[df_1['PRNAME'] == province]
    
    # converting filtered dataset to json
    geojson_data = df.to_json()
    
    # getting the bounds for visualization
    bounds = folium.GeoJson(geojson_data).get_bounds()

    # calculating the center of the bounds
    center = [(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2]

    # Folium interactive map
    m = folium.Map(location=center, width="%100", height="%100", zoom_start=5)

    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': 'green' if feature['properties']['target'] == 'reached' else 'red',
            'color':'black',
            'weight': 0.5,
            'fillOpacity':2
        },highlight_function=lambda x: {'weight': 3, 'color': 'red'},
        smooth_factor=2.0,
        tooltip=folium.GeoJsonTooltip(
            fields=['Income percentile', "Pop_2021", "PCNAME", 'target', 'avg_d_kbps'],
            aliases=['Income percentile', 'Population_2021', 'Town', '50/10 target', 'avg_d_kbps'],
            localize=True,
        )
    ).add_to(m)

    # making the map responsive to change in layout size
    make_map_responsive= """
    <style>
    [title~="st.iframe"] { width: 100%; height:800px}
    </style>
    """
    st.markdown(make_map_responsive, unsafe_allow_html=True)
    return folium_static(m)

# calling the visualization
plot_target(province_1)



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
st.write(" ")
st.write(" ")

# subheader of second visualization
st.subheader(f'#2. What is the distribution of Median Income in "{province_1}"?')

# creating the folim map
@st.cache_resource
def plot_income_percentile(province):
    df = df_1[df_1['PRNAME'] == province]
    
    # converting filtered dataset to json
    geojson_data = df.to_json()
    
    # getting the bounds for visualization
    bounds = folium.GeoJson(geojson_data).get_bounds()

    # calculating the center of the bounds
    center = [(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2]

    # Folium interactive map
    m = folium.Map(location=center, width="%100", height="%100", zoom_start=5)

    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': '#FF0022' if feature['properties']['Income percentile'] == '0-25pct' else
            ('#F2A900' if feature['properties']['Income percentile'] == '25-50pct' else
            ('#E0F200' if feature['properties']['Income percentile'] == '50-75pct' else 
            ('#00F237' if feature['properties']['Income percentile'] == '75-100pct' else '#EBEBEB'))),
            'color':'black',
            'weight': 0.5,
            'fillOpacity':2
        },highlight_function=lambda x: {'weight': 3, 'color': 'red'},
        smooth_factor=2.0,
        tooltip=folium.GeoJsonTooltip(
            fields=['Income percentile', "Pop_2021", "PCNAME", 'target', 'avg_d_kbps'],
            aliases=['Income percentile', 'Population_2021', 'Town', '50/10 target', 'avg_d_kbps'],
            localize=True,
        )
    ).add_to(m)

    make_map_responsive= """
    <style>
    [title~="st.iframe"] { width: 100%; height:1000px}
    </style>
    """
    st.markdown(make_map_responsive, unsafe_allow_html=True)
    return folium_static(m)


# visualizing the income percentile
plot_income_percentile(province_1)



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@st.cache_data
def process_z_score_data():
    return process_data.speed_z_score()

# calling dataframe 2 from module
df_2 = process_z_score_data()


st.write(" ")
st.write(" ")

# subheader of third visualization
st.subheader(f'#3. How are internet download speeds distributed across "{province_1}"?')

@st.cache_resource
def plot_speed_z_score(province):
    df = df_2[df_2['PRNAME'] == province]

    # getting the min and max values of speed_z_score for colormap scaling
    min_speed_z_score = df['speed_z-score'].min()
    max_speed_z_score = df['speed_z-score'].max()

    # defining a colormap (e.g., 'coolwarm') for speed_z_score
    colormap = cm.get_cmap('seismic')

    # creating a color function to map speed_z_score to colors
    def color_function(feature):
        speed_z_score = feature['properties']['speed_z-score']

        # Checking if speed_z_score for this specific feature is NaN
        if pd.isna(speed_z_score):
            return "#00000000"  

        # Continuing with normalization and colormap for valid speed_z_score values
        normalized_speed_z_score = (speed_z_score - min_speed_z_score) / (max_speed_z_score - min_speed_z_score)
        color = colormap(normalized_speed_z_score)
        return f"rgb({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)})"

    # Converting the filtered dataset to JSON
    geojson_data = df.to_json()

    # Getting the bounds for visualization
    bounds = folium.GeoJson(geojson_data).get_bounds()

    # Calculating the center of the bounds
    center = [(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2]

    # Folium interactive map
    m = folium.Map(location=center, width="%100", height="%100", zoom_start=5)

    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': color_function(feature),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 5
        },
        highlight_function=lambda x: {'weight': 3, 'color': 'red'},
        smooth_factor=2.0,
        tooltip=folium.GeoJsonTooltip(
            fields=["Pop_2021", "PCNAME", 'avg_d_kbps', 'speed_z-score'],
            aliases=['Population_2021', 'Town', 'avg_d_kbps', 'Speed Z-Score'],
            localize=True,
        )
    ).add_to(m)
    
    make_map_responsive= """
    <style>
    [title~="st.iframe"] { width: 100%; height:1000px}
    </style>
    """
    
    st.markdown(make_map_responsive, unsafe_allow_html=True)
    return folium_static(m)

# calling the map visualization
plot_speed_z_score(province_1)




# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@st.cache_data
def process_speed_income_data():
    return process_data.speed_income_ratio()

# calling dataframe 3 from module
df_3 = process_speed_income_data()

st.write(" ")
st.write(" ")

# subheader of fourth visualization
st.subheader(f'#4. Is there a correlation between Internet download speed and Median income in "{province_1}"?')

@st.cache_resource
def plot_speed_income_ratio(province):
    df = df_3[df_3['PRNAME'] == province]

    # getting the min and max values of speed_income_ratio for colormap scaling
    min_speed_income_ratio = df['speed_income_ratio'].min()
    max_speed_income_ratio = df['speed_income_ratio'].max()

    # defining a colormap (e.g., 'coolwarm') for speed_income_ratio
    colormap = cm.get_cmap('seismic')

    # creating a color function to map speed_income_ratio to colors
    def color_function(feature):
        speed_income_ratio = feature['properties']['speed_income_ratio']

        # checking if speed_income_ratio for this specific feature is NaN
        if pd.isna(speed_income_ratio):
            return "#00000000"  

        # continuing with normalization and colormap for valid speed_income_ratio values
        normalized_speed_income_ratio = (speed_income_ratio - min_speed_income_ratio) / (max_speed_income_ratio - min_speed_income_ratio)
        color = colormap(normalized_speed_income_ratio)
        return f"rgb({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)})"

    # converting the filtered dataset to JSON
    geojson_data = df.to_json()

    # Getting the bounds for visualization
    bounds = folium.GeoJson(geojson_data).get_bounds()

    # Calculating the center of the bounds
    center = [(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2]

    # Folium interactive map
    m = folium.Map(location=center, width="%100", height="%100", zoom_start=5)

    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': color_function(feature),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 5
        },
        highlight_function=lambda x: {'weight': 3, 'color': 'red'},
        smooth_factor=2.0,
        tooltip=folium.GeoJsonTooltip(
            fields=["Pop_2021", "PCNAME", 'avg_d_kbps', 'speed_income_ratio'],
            aliases=['Population_2021', 'Town', 'avg_d_kbps', 'Speed:Income ratio'],
            localize=True,
        )
    ).add_to(m)
    
    make_map_responsive= """
    <style>
    [title~="st.iframe"] { width: 100%; height:1000px}
    </style>
    """
    
    st.markdown(make_map_responsive, unsafe_allow_html=True)
    return folium_static(m)

# calling the map visualization
plot_speed_income_ratio(province_1)



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# returns target data
@st.cache_data
def percentile_data(province_1):
    return process_data.process_percentile_data(province_1)

# calling percentile dataframe from module
percentile_df = percentile_data(province_1)

# returns plot
@st.cache_resource
def plot_percentile_data(df, province):
    return process_data.plot_percentile(df, province)

st.write(" ")
st.write(" ")

# subheader of fifth visualization
st.subheader(f'#5. Internet download speed by Income percentile in "{province_1}"?')

fig_1 = plot_percentile_data(percentile_df, province_1)

# showing the plot
st.pyplot(fig_1)



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# returns target data
@st.cache_data
def target_data(province_1):
    return process_data.process_yearly_target_data(province_1)

# calling the target dataframe from module
target_df = target_data(province_1)

# returns plot
@st.cache_resource
def plot_target_data(df, province):
    return process_data.plot_yearly_target(df, province)

st.write(" ")
st.write(" ")

# subheader of sixth visualization
st.subheader(f'#6. Number of towns that did not meet the 50/10 target in "{province_1}"?')

fig_2 = plot_target_data(target_df, province_1)

# showing the plot
st.pyplot(fig_2)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
st.write(" ")
st.write(" ")

# subheader of seventh visualization
st.subheader('#7. Internet download speed in Urban vs Rural areas')

img_path = "/home/ubuntu/ookla-statcan-analysis-group1/notebooks/hackathon/urban_rural_speeds.jpg"

# showing the image
st.image(img_path)



