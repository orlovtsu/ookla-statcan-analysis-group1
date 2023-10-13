# importing packages
import sys
sys.path.append("/home/ubuntu/ookla-statcan-analysis-group1/")

# importing packages
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.lines as lines
import geopandas as gp

from src.config import DATA_DIRECTORY
import warnings
warnings.filterwarnings('ignore')


# loading the data
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

# Processing our streamlit data
# ================================================================================================================
def income_pct():
    province_data = full_data.copy()
    avg_income = province_data.groupby(['PRNAME','PCNAME'])[['Median_income']].mean().reset_index()
    last_row = avg_income[-1:]
    avg_income = avg_income[:-1]
    avg_income['pct'] = avg_income.groupby('PRNAME')['Median_income'].transform(
        lambda x: pd.qcut(x, q=[0, 0.25, 0.5, 0.75, 1.0], labels=['0-25pct', '25-50pct', '50-75pct', '75-100pct'], duplicates='drop'))
    
    last_row.loc[:, 'pct'] = 'nan'
    avg_income = pd.concat((avg_income, last_row))
    
    avg_income.rename({
        'Median_income': 'Median_income_city',
        'pct': 'Income percentile'
    }, axis=1, inplace=True)
    
    das_info_copy = pd.merge(das_info, avg_income, how='outer', on=['PRNAME','PCNAME'])

    speed_data_grouped = speed_data.groupby('DAUID')[['year', 'quarter', 'avg_d_kbps', 'avg_u_kbps', 'devices']].mean().reset_index()

    das_info_copy = pd.merge(das_info_copy, speed_data_grouped)
    
    das_info_copy['target'] = np.where((das_info_copy['avg_d_kbps'] >= 51_200.) & (das_info_copy['avg_u_kbps'] >= 10_240.), 'reached', 'did not')
    
    return das_info_copy



# 2. visualization I
def process_percentile_data(province):
    das_info_copy = income_pct()
    df_percentile = das_info_copy.groupby(["PRNAME", "Income percentile"])['avg_d_kbps'].mean().reset_index()
    df_percentile.dropna(inplace=True)
    df = df_percentile[df_percentile['PRNAME'] == province].reset_index(drop=True)
    
    return df


def plot_percentile(df, province):
    background_color='#fafafa'
    
    fig, ax = plt.subplots(figsize=(15,10))
    fig.patch.set_facecolor(background_color) # figure background color
    ax.set_facecolor(background_color)
    
    max_val = df['avg_d_kbps'].max()
    colors = ['#F9EEEE' if value != max_val else '#FC3636' for value in df['avg_d_kbps']]
    
    ax.bar(df['Income percentile'], df['avg_d_kbps'], width=.6, ec='k', lw=4, color=colors)
    
    def y_axis_formatter(value, pos):
        return int(value/1000)
    
    # Apply the y-axis label formatting function
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
    ax.set_ylabel("Internet download speed (mb/s)", fontfamily='monospace', fontsize=15, color='k')
    ax.set_xlabel("Income percentile", fontfamily='monospace', fontsize=15, color='k')

    fig.text(0.12, 1, f"Internet download speed by Income Percentile in {province}", color='k', weight='bold',
                fontfamily='monospace', fontsize=20, ha='left', va='top')
    
    max_idx = df['avg_d_kbps'].idxmax()
    if max_idx == 2:
        fig.text(1.07, 0.78, f"""
    In {province}, people belonging to the {df['Income percentile'][max_idx]} 
    have higher internet download speeds than others.
    
    Which is similar to most provinces in Canada.
    """,
            fontsize=15, fontfamily='monospace', color='k')
    else:
        fig.text(1.07, 0.78, f"""
    In {province}, people belonging to the {df['Income percentile'][max_idx]} 
    have higher internet download speeds than others.
    """,
            fontsize=15, fontfamily='monospace', color='k')
    
    
    fig.text(1.6, 0.8, " ")

    for s in ['top','right']:
        ax.spines[s].set_visible(False)
    
    ax.axhline(y=0, color='k', lw=5, alpha=1)
    ax.grid(False)

    l1 = lines.Line2D([1.0, 1.0], [0.05, 1.0], transform=fig.transFigure, figure=fig, color='k', lw=0.2)
    fig.lines.extend([l1])
    
    return fig
    
    


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  
def process_yearly_target_data(province):
    df_town_target = full_data[['year', 'PRNAME', 'PCNAME', 'Median_income', 'avg_d_kbps', 'avg_u_kbps']]
    df_town_target=df_town_target.groupby(['year', 'PRNAME', 'PCNAME']).agg({'avg_u_kbps':'mean', 'avg_d_kbps':'mean', 'Median_income': 'mean'}).reset_index()
    df_town_target['target'] = np.where((df_town_target['avg_d_kbps'] >= 51_200.) & (df_town_target['avg_u_kbps'] >= 10_240.), 'reached', 'did not')
    
    did_not_reach_target = df_town_target[df_town_target['target'] == 'did not'][['year','PRNAME','PCNAME','Median_income']]
    did_not_reach_target.dropna(inplace=True)
    did_not_reach_target=did_not_reach_target.groupby(['year','PRNAME']).agg({'PCNAME':'count', 'Median_income': 'mean'}).reset_index()
    
    df = did_not_reach_target[did_not_reach_target['PRNAME'] == province]
    df = df.reset_index(drop=True)
    
    return df


def plot_yearly_target(df, province):
    background_color='#fafafa'
    
    fig, ax = plt.subplots(figsize=(15,10))
    fig.patch.set_facecolor(background_color) # figure background color
    ax.set_facecolor(background_color)
    
    ax.plot(df['year'], df['PCNAME'], '-', marker='o', color='#32960C', lw=3, markersize=13)
    for idx in range(df.shape[0]):
        plt.annotate(xy=(df['year'][idx], df['PCNAME'][idx]+0.4), text=df['year'][idx], fontsize=15, fontfamily='monospace', ha='center', va='bottom')

    
    for s in ['top','right']:
        ax.spines[s].set_visible(False)
    
    ax.set_xticks([])
    ax.set_ylim([0,df['PCNAME'].max() + 10])
    ax.set_ylabel("No. of towns", fontfamily='monospace', fontsize=15, color='k')
    
    fig.text(0.12, 0.95, f"Number of towns that did not meet 50/10 target in {province}", color='k', weight='bold',
            fontfamily='monospace', fontsize=20, ha='left', va='top')
    fig.text(0.15, .35, 
            f"""As of 2023, the number of towns that do not 
meet the 50/10 target has reduced by {(df['PCNAME'][0] - df['PCNAME'].tolist()[-1]) / df['PCNAME'][0]:.1%} 
compared to 2019""", 
             color='k', fontfamily='monospace', fontsize=10, ha='left', va='top')

    ax.axhline(y=0, color='k', lw=5, alpha=1)
    plt.grid(False)
    
    return fig



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def internet_deviation(data):
    std = data['avg_d_kbps'].std()
    mean = data['avg_d_kbps'].mean()

    return (data['avg_d_kbps'] - mean) / std


def provincial_data():
    das_info_copy = income_pct()
    df_prv = das_info_copy.groupby(['PRNAME','PCNAME'])[['Median_income_city','avg_d_kbps', 'avg_u_kbps']].mean().reset_index()
    
    return df_prv


def speed_z_score():
    df_prv = provincial_data()
    das_info_copy = income_pct()
    df_prv['speed_z-score'] = df_prv.groupby(['PRNAME']).apply(internet_deviation).reset_index()['avg_d_kbps']
    df_std = df_prv[['PRNAME', 'PCNAME','speed_z-score']]
    das_info_copy = das_info_copy.merge(df_std, on=['PRNAME', 'PCNAME'], how='outer')
    
    return das_info_copy


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def speed_income_ratio():
    df_prv = provincial_data()
    das_info_copy = income_pct()
    # calculating the speed:income ratio
    df_prv['speed_income_ratio'] = df_prv['avg_d_kbps'] / df_prv['Median_income_city']
    df_speed_income = df_prv[['PRNAME', 'PCNAME','speed_income_ratio']]
    das_info_copy = das_info_copy.merge(df_speed_income, on=['PRNAME', 'PCNAME'], how='outer')
    
    return das_info_copy