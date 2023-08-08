import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, datetime, timedelta, date
from neuralprophet import NeuralProphet
import warnings
import os


warnings.filterwarnings('ignore')

def run_predicion_model():
    df = pd.read_csv("datasets/weatherdata.csv")
    df['time_stamp'] = pd.to_datetime(df['time_stamp'])
    df.set_index('time_stamp')
    temp = df.drop('time_stamp', axis=1)
    df['date'] = df['time_stamp'].dt.date
    df['year'] = df['time_stamp'].dt.year
    df['month'] = df['time_stamp'].dt.month


    df1 = df[df['date'] >= date(2017,1,1)]
    dfbefore2021 = df[df['year']<2021]

    df = pd.read_csv("datasets/weatherdata.csv")[['time_stamp', 'temperature']]
    df.time_stamp = pd.to_datetime(df.time_stamp)

    df.rename(columns = {'time_stamp':'ds', 'temperature':'y'}, inplace = True)

    m = NeuralProphet(changepoints_range=0.95, 
                    n_changepoints=50, 
                    trend_reg=1, 
                    weekly_seasonality=False, 
                    daily_seasonality=10, 
                    yearly_seasonality=10)
    
    df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
    metrics = m.fit(df_train, freq='H', validation_df=df_val)

    df['ds'] = pd.DatetimeIndex(df['ds'])

    future = m.make_future_dataframe(df, periods=24*365*3, n_historic_predictions=len(df))

    forecast = m.predict(future)

    forecast.to_csv( "outputs/temperature_prediction.csv", index=False)


    """# <a>Wind Speed</a>"""

    df = pd.read_csv("datasets/weatherdata.csv")[['time_stamp', 'wind_speed']]

    df.time_stamp = pd.to_datetime(df.time_stamp)


    monthlywind = pd.DataFrame(dfbefore2021.groupby(['month'])['wind_speed'].mean())
    months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
    monthlywind['Month']=months


    df.rename(columns = {'time_stamp':'ds', 'wind_speed':'y'}, inplace = True)

    m = NeuralProphet(changepoints_range=0.95, 
                    n_changepoints=50, 
                    trend_reg=1, 
                    weekly_seasonality=False, 
                    daily_seasonality=10, 
                    yearly_seasonality=10)
    
    df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
    metrics = m.fit(df_train, freq='H', validation_df=df_val)

    df['ds'] = pd.DatetimeIndex(df['ds'])


    future = m.make_future_dataframe(df, periods=24*365*3, n_historic_predictions=len(df))
    forecast = m.predict(future)

    forecast.to_csv( "outputs/windspeed_prediction.csv", index=False)

    """# <a>Pressure</a>"""

    df = pd.read_csv("datasets/weatherdata.csv")[['time_stamp', 'mean_sea_level_pressure']]
    df.time_stamp = pd.to_datetime(df.time_stamp)

    monthlypressure = pd.DataFrame(dfbefore2021.groupby(['month'])['mean_sea_level_pressure'].mean())
    months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
    monthlypressure['Month']=months

    df.rename(columns = {'time_stamp':'ds', 'mean_sea_level_pressure':'y'}, inplace = True)


    m = NeuralProphet(changepoints_range=0.95, 
                    n_changepoints=50, 
                    trend_reg=1, 
                    weekly_seasonality=False, 
                    daily_seasonality=10, 
                    yearly_seasonality=10)

    df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
    metrics = m.fit(df_train, freq='H', validation_df=df_val)
    df['ds'] = pd.DatetimeIndex(df['ds'])


    future = m.make_future_dataframe(df, periods=24*365*3, n_historic_predictions=len(df))
    forecast = m.predict(future)

    forecast.to_csv( "outputs/pressure_prediction.csv", index=False)

    """# <a>Total Cloud Cover</a>"""

    df = pd.read_csv("datasets/weatherdata.csv")[['time_stamp', 'total_cloud_cover']]
    df.time_stamp = pd.to_datetime(df.time_stamp)




    monthlycloud = pd.DataFrame(dfbefore2021.groupby(['month'])['total_cloud_cover'].mean())
    months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
    monthlycloud['Month']=months


    df.rename(columns = {'time_stamp':'ds', 'total_cloud_cover':'y'}, inplace = True)




    m = NeuralProphet(changepoints_range=0.95, 
                    n_changepoints=50, 
                    trend_reg=1, 
                    weekly_seasonality=False, 
                    daily_seasonality=10, 
                    yearly_seasonality=10)

    df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
    metrics = m.fit(df_train, freq='H', validation_df=df_val)
    df['ds'] = pd.DatetimeIndex(df['ds'])


    future = m.make_future_dataframe(df, periods=24*365*3, n_historic_predictions=len(df))
    forecast = m.predict(future)


    forecast.to_csv( "outputs/cloudcover_prediction.csv", index=False)

    temp= pd.read_csv('outputs/temperature_prediction.csv')
    cloudcover= pd.read_csv('outputs/cloudcover_prediction.csv')
    pressure= pd.read_csv('outputs/pressure_prediction.csv')
    wind= pd.read_csv('outputs/windspeed_prediction.csv')

    new= temp["ds"].str.split(" ", n = 1, expand = True)
    temp['datestamp'] = pd.to_datetime(temp['ds'])
    temp['date'] = new[0]
    temp['time'] = new[1]
    temp['hour'] = temp['datestamp'].dt.hour

    new= cloudcover["ds"].str.split(" ", n = 1, expand = True)
    cloudcover['datestamp'] = pd.to_datetime(cloudcover['ds'])
    cloudcover['date'] = new[0]
    cloudcover['time'] = new[1]
    cloudcover['hour'] = cloudcover['datestamp'].dt.hour
    cloudcover['date'] = new[0]
    cloudcover['time'] = new[1]

    new= wind["ds"].str.split(" ", n = 1, expand = True)
    wind['datestamp'] = pd.to_datetime(wind['ds'])
    wind['date'] = new[0]
    wind['time'] = new[1]
    wind['hour'] = wind['datestamp'].dt.hour
    wind['date'] = new[0]
    wind['time'] = new[1]

    new= pressure["ds"].str.split(" ", n = 1, expand = True)
    pressure['datestamp'] = pd.to_datetime(pressure['ds'])
    pressure['date'] = new[0]
    pressure['time'] = new[1]
    pressure['hour'] = pressure['datestamp'].dt.hour
    pressure['date'] = new[0]
    pressure['date'] = new[1]

    final =pd.DataFrame()

    final['datestamp'] = temp['datestamp'].astype(str)
    final['date'] = temp['date']
    final['time'] = temp['time']
    final['hour'] = temp['hour']
    final['temperature'] = temp['yhat1']
    final['windspeed'] = wind['yhat1']
    final['pressure'] = pressure['yhat1']
    final['cloudcover'] = cloudcover['yhat1']

    final.to_csv('outputs/allpredicted.csv',index=False)

def get_today_weather_state():
    
    df = pd.read_csv('outputs/allpredicted.csv')
    today_date = datetime.now().strftime('%Y-%m-%d')
    today_df = df[df['date']==today_date]
    avg_df = today_df.groupby('date').mean()
    json_data = avg_df.to_dict(orient='records')
    return json_data[0]

def get_weather_state_day(day):

    df = pd.read_csv('outputs/allpredicted.csv')
    day_df = df[df['date']==day]
    json_data = day_df.to_dict(orient='records')
    return json_data

def get_monthly_data():
    df = pd.read_csv('outputs/allpredicted.csv')
    today_date = datetime.now().strftime('%Y-%m-%d')
    upto_today_df = df[df['date'] <= today_date]
    avg_df = upto_today_df.groupby('date').mean()
    avg_df['date'] = avg_df.index
    avg_df = avg_df.tail(30)
    return avg_df.to_dict(orient='records')


