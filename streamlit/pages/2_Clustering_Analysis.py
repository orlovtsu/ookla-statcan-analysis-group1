import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

import load_data

def input_variables(provinces):
    #provinces
    province = st.sidebar.selectbox('Select province:', provinces, index = 8)
    data ={
        'province': province
    }
    return data

st.set_page_config(
    page_title="Clustering analysis",
    layout="wide"
)
st.sidebar.header('Clustering analysis')
    
df_provinces, status = load_data.load_provinces()


features = input_variables(df_provinces['PRNAME'].unique())
province = features['province']

st.write(f'# List of areas which are not achieved 50/10 goal in `{province}`')


df0, status = load_data.load_clusters()

df0.rename(columns = {'avg_d_kbps': 'avg_d_kbps_fixed', 'avg_u_kbps': 'avg_u_kbps_fixed'}, inplace = True)
df_cl = df0[((df0['avg_d_kbps_fixed']/1024 < 50) & (df0['avg_u_kbps_fixed']/1024 < 10)) &
         ((df0['avg_d_kbps_mobile']/1024 < 50) & (df0['avg_u_kbps_mobile']/1024 < 10)) & 
         (df0['PRNAME'] == province)]
st.write(df_cl[['DAUID', 'PRNAME', 'PCNAME', 'avg_d_kbps_fixed', 'avg_u_kbps_fixed', 'avg_d_kbps_mobile', 'avg_u_kbps_mobile']].sort_values(by = 'avg_d_kbps_fixed', ascending = True))

area_list = df_cl['DAUID'] + '-' + df_cl['PCNAME']
selected_area = st.selectbox('Select area:', area_list)

st.write(f"# List of the most similar to `{selected_area}`areas to learn from")
#st.write(df0[df0['DAUID'] == selected_area[:8]].iloc[0]['Clusters'])
st.write(df0[(df0['Clusters'] == df0[df0['DAUID'] == selected_area[:8]].iloc[0]['Clusters']) & 
             (df0['PRNAME'] == province)][['DAUID', 'PRNAME', 'PCNAME', 'avg_d_kbps_fixed', 'avg_u_kbps_fixed', 'avg_d_kbps_mobile', 'avg_u_kbps_mobile']].sort_values(by = 'avg_d_kbps_fixed', ascending = False))