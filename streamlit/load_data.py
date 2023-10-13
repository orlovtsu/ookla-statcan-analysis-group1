import pandas as pd
import geopandas as gp
from src.config import DATA_DIRECTORY
import streamlit as st

@st.cache_data
def load_data():
    try:
        das_info = gp.read_file(DATA_DIRECTORY / "hackathon" / "geometry.gpkg", driver="GPKG")
        speed_data = pd.read_csv(DATA_DIRECTORY / "hackathon" / "speeds.csv")
        speed_data.DAUID = speed_data.DAUID.astype(str)
        full_data = pd.merge(das_info, speed_data)
        full_data["date"] = pd.to_datetime(
                full_data["year"].astype(str)
                + "-"
                + ((full_data["quarter"] - 1) * 3 + 1).astype(str)
                + "-01"
        )
        years = speed_data['year'].unique()
        df = full_data[full_data['year'].isin(years[:4]) | 
                   full_data['quarter'].isin([1,2])]
        status = True
    except:
        df = pd.DataFrame()
        status = False
    return df, status

@st.cache_data
def load_speed_data():
    try:
        df = pd.read_csv(DATA_DIRECTORY / "hackathon" / "speeds.csv")
        df.DAUID = df.DAUID.astype(str)
        years = df['year'].unique()
        df = df[df['year'].isin(years[:4]) | 
            df['quarter'].isin([1,2])]
        status = True
    except:
        df = pd.DataFrame()
        status = False
    return df, status 

@st.cache_data
def load_provinces():
    try:
        df = pd.read_csv(DATA_DIRECTORY / "hackathon" / "dauid_provinces.csv")
        df.DAUID = df.DAUID.astype(str)
        status = True
    except:
        df = pd.DataFrame()
        status = False
    return df, status 


def load_stats():
    try:
        df_pop = pd.read_csv(DATA_DIRECTORY / "hackathon" / 'canada_population.csv')
        df_stats = pd.read_csv(DATA_DIRECTORY / "hackathon" / 'stats.csv')
        status = True
    except:
        df_pop = pd.read_csv('canada_population.csv')#pd.DataFrame()
        df_stats = df_pop
        status = False
    return df_pop, df_stats, status