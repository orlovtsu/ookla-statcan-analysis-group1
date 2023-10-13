import load_data
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import statsmodels.api as sm

def input_variables(provinces, metrics, forecast_periods):
    st.sidebar.write('### Historical Data:')
    metric = st.sidebar.selectbox('Select metric:', metrics)
    st.sidebar.write('#####  Provinces')

    prov = list([0] * len(provinces))
    for i, prname in enumerate(provinces):
        prov[i] = st.sidebar.checkbox(prname, value = True)
    st.sidebar.write("Forecast:")
    metrics2 = metrics
    metric2 = st.sidebar.selectbox('Select metric to forecast:', metrics2)
    prov_forecast = st.sidebar.selectbox('Select province to forecast:', provinces)
    period_forecast = st.sidebar.select_slider('Select forecast period:',
                    options = forecast_periods,
                               value = forecast_periods[3])

    show_prov = prov*provinces
    show_prov = list(filter(lambda item: item != '', show_prov.tolist()))
    data = {'show_prov': show_prov, 
            'metric': metric,
            'metric_forecast': metric2,
            'province_forecast': prov_forecast,
            'period_forecast': period_forecast}
 
    return data

st.set_page_config(
    page_title="Time Series Analysis",
    layout="wide"
)

st.write("""
# Time Series Analysis
""")

df, status = load_data.load_speed_data()

# if status:
#     st.success('Data Loaded')
# else:
#     st.error('Data can not be loaded')

df_provinces, status = load_data.load_provinces()

# if status:
#     st.success('Provinces Loaded')
# else:
#     st.error('Provinces DAUIDs can not be loaded')

df = pd.merge(df, df_provinces, on = 'DAUID', how = 'left')

grouped = df.groupby(['year', 'quarter', 'PRNAME', 'conn_type']).agg({
    'avg_d_kbps': 'mean',
    'avg_u_kbps': 'mean',
}).unstack('conn_type').reset_index()
grouped['year-quarter'] = grouped['year'].astype(str) + '-' + grouped['quarter'].astype(str)
grouped.columns = [f'{col[0]}_{col[1]}' if col[1] else col[0] for col in grouped.columns]
df1 = grouped.rename(columns={
    'PRNAME': 'province',
    'year-quarter': 'year-quarter',
    'avg_d_kbps_fixed': 'avg_fixed_d_kbps',
    'avg_u_kbps_fixed': 'avg_fixed_u_kbps',
    'avg_d_kbps_mobile': 'avg_mobile_d_kbps',
    'avg_u_kbps_mobile': 'avg_mobile_u_kbps'
})
metrics = ['avg_fixed_d_kbps','avg_fixed_u_kbps','avg_mobile_d_kbps','avg_mobile_u_kbps']
forecast_periods = ['2023-3', '2023-4', '2024-1', '2024-2', '2024-3', '2024-4',  '2025-1', '2025-2', '2025-3', '2025-4',
                    '2025-1', '2025-2', '2025-3', '2025-4', '2026-1', '2026-2', '2026-3', '2026-4']
features = input_variables(df1['province'].unique(), metrics, forecast_periods)
show_prov = features['show_prov']#[features.show_prov != ''].values.tolist()
metric = features['metric']
metric_forecast = features['metric_forecast']
province_forecast = features['province_forecast']
period_forecast = features['period_forecast']

st.write('### Historical data of average internet speed data by province')
plt.figure(figsize=(10, 4))
for province in show_prov:
    df_prov = df1[df1['province'] == province]
    plt.plot(df_prov['year-quarter'], df_prov[metric]/1024, label = province)
    plt.annotate(province, xy=(df_prov['year-quarter'].iloc[-1], df_prov[metric].iloc[-1]/1024))
plt.xlabel('Quarter')
plt.ylabel('Mbps')
plt.xticks(rotation = 90)

st.pyplot(plt)

st.write(f'### Forecast of `{metric_forecast}` for {province_forecast}')
df_forecast = df1[df1['province'] == province_forecast]
model2 = sm.tsa.ARIMA(df_forecast[metric_forecast],order=(4,1,6))
results = model2.fit()

forecast = results.get_forecast(steps=forecast_periods.index(period_forecast)+1)
mean = forecast.predicted_mean
conf_int = forecast.conf_int()
d = mean.index
forecast_steps = [str(2019+x//4) + '-' + str((x)%4+1) for x in d]

plt.figure(figsize=(10,4))
plt.plot(df_forecast['year-quarter'], df_forecast[metric_forecast]/1024, label='Oiginal', color = 'red')
plt.plot(forecast_steps, mean/1024, label='Forecasted', color= 'green')
plt.fill_between(d, conf_int.iloc[:,0]/1024, conf_int.iloc[:,1]/1024, alpha=0.2, color= 'blue')
plt.ylabel('Mbps')
plt.xticks(rotation = 90)
plt.legend()

st.pyplot(plt)

st.write(f'Forecasted average `{metric_forecast}` speed in {period_forecast} in {province_forecast}:')
st.write(f'Average: {mean.iloc[-1]/1024:.2f} MBps')
st.write(f'Confidence interval: [{conf_int.iloc[-1,0]/1024:.2f}, {conf_int.iloc[-1,1]/1024:.2f}]')