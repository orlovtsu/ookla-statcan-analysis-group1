import pandas
import matplotlib.pyplot as plt
import streamlit as st
from src.config import DATA_DIRECTORY

import load_data

st.set_page_config(
    page_title="Statistics",
    layout="wide"
)
st.sidebar.header('What is 50/10 internet speed goal?')
st.sidebar.markdown("""
Canada’s Connectivity Strategy, released in 2019, committed to ensuring all Canadians have access to high-speed Internet at speeds of at least 50 Megabits 
per second (Mbps) download / 10 Mbps upload. 
            
**2026 Target** - 98.7% of all households 
            
**2030 Target** - 100% of all households 
""")
#st.sidebar.success('Statistics')

status = False
#df, status = load_data.load_data()

if status:
    st.success('Data Loaded')

st.markdown("""
# Achievement of 50/10 internet speed goal in Canada 
### The state in the second quarter of 2023

""")

st.write("""
In **2023** the current state is different for different territories and areas, especially for urban and rural territories.
In **2023** population of Canadians is distributed between urban and rural territories:
         

""")

green_colors = ['#4CAF50', '#8BC34A', '#CDDC39']
red_colors = ['#F44336', '#E91E63', '#FF9800']

df_pop, df_stats, status = load_data.load_stats()

plot1 = plt.figure(figsize=(3,3)) 
color_map = [green_colors[0], red_colors[0]]
urban_prop = (df_pop['Urban']/df_pop['Overall']).iloc[0]
rural_prop = (df_pop['Rural']/df_pop['Overall']).iloc[0]
plt.pie([urban_prop, 1 - urban_prop], explode = [0, 0.1], labels = ['Urban', 'Rural'], colors = color_map, autopct='%1.2f%%', startangle = 39)
st.pyplot(plot1, use_container_width=False)

st.write("### Proportion of urban areas in Canada connected to the internet with speed 50/10 in 2 quarter of 2023")

#st.write(df_stats)
color_map = [green_colors[0], red_colors[0]]
color_map1 = [green_colors[1], red_colors[1]]
color_map2 = [green_colors[2], red_colors[2]]
plot2, ax = plt.subplots(1, 3, figsize =  (15, 6))
row = df_stats[df_stats['Indicator'] == 'AreaUrban']
overall, fixed, mobile = row['Overall'].iloc[0], row['Fixed'].iloc[0], row['Mobile'].iloc[0]
ax[0].pie([overall, 1-overall], explode = [0, 0.1],colors = color_map, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 39)
ax[1].pie([fixed, 1-fixed], explode = [0, 0.1],colors = color_map1, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 39)
ax[2].pie([mobile, 1-mobile], explode = [0, 0.1],colors = color_map2, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 100)
ax[0].set_title('Mobile or fixed')
ax[1].set_title('Fixed')
ax[2].set_title('Mobile')

st.pyplot(plot2)

st.write("### Proportion of urban population in Canada connected to the internet with speed 50/10 in 2 quarter of 2023")

plot3, ax = plt.subplots(1, 3, figsize =  (15, 6))
row = df_stats[df_stats['Indicator'] == 'PopUrban']
overall, fixed, mobile = row['Overall'].iloc[0], row['Fixed'].iloc[0], row['Mobile'].iloc[0]
ax[0].pie([overall, 1-overall], explode = [0, 0.1],colors = color_map, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 39)
ax[1].pie([fixed, 1-fixed], explode = [0, 0.1],colors = color_map1, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 39)
ax[2].pie([mobile, 1-mobile], explode = [0, 0.1],colors = color_map2, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 100)
ax[0].set_title('Mobile or fixed')
ax[1].set_title('Fixed')
ax[2].set_title('Mobile')
st.pyplot(plot3)
st.write("### Proportion of rural areas in Canada connected to the internet with speed 50/10 in 2 quarter of 2023")

plot3, ax = plt.subplots(1, 3, figsize =  (15, 6))
row = df_stats[df_stats['Indicator'] == 'AreaRural']
overall, fixed, mobile = row['Overall'].iloc[0], row['Fixed'].iloc[0], row['Mobile'].iloc[0]
ax[0].pie([overall, 1-overall], explode = [0, 0.1],colors = color_map, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 60)
ax[1].pie([fixed, 1-fixed], explode = [0, 0.1],colors = color_map1, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 60)
ax[2].pie([mobile, 1-mobile], explode = [0, 0.1],colors = color_map2, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 160)
ax[0].set_title('Mobile or fixed')
ax[1].set_title('Fixed')
ax[2].set_title('Mobile')
st.pyplot(plot3)

st.write("### Proportion of rural population in Canada connected to the internet with speed 50/10 in 2 quarter of 2023")

plot3, ax = plt.subplots(1, 3, figsize =  (15, 6))
row = df_stats[df_stats['Indicator'] == 'PopRural']
overall, fixed, mobile = row['Overall'].iloc[0], row['Fixed'].iloc[0], row['Mobile'].iloc[0]
ax[0].pie([overall, 1-overall], explode = [0, 0.1],colors = color_map, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 60)
ax[1].pie([fixed, 1-fixed], explode = [0, 0.1],colors = color_map1, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 60)
ax[2].pie([mobile, 1-mobile], explode = [0, 0.1],colors = color_map2, labels = ['achieved', 'not achieved'], autopct='%1.2f%%',
        startangle = 160)
ax[0].set_title('Mobile or fixed')
ax[1].set_title('Fixed')
ax[2].set_title('Mobile')
st.pyplot(plot3)