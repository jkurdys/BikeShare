import pandas as pd
import numpy as np
import datetime as dt

def retrieve_data(cloned = True):
    '''
    If running the function runs from the cloned repo, no file path
    will be required. Otherwise, the appropriate path must be
    supplied as a string.

    Returns stations, trips and weather data frames, respectively.
    '''
    if cloned:
        stations = pd.read_csv('/Users/Diogenes/Documents/take_homes/BikeShare/data/station_data.csv')
        trips = pd.read_csv('/Users/Diogenes/Documents/take_homes/BikeShare/data/trip_data.csv',
                        parse_dates=['Start Date', 'End Date'], 
                        infer_datetime_format=True)
        weather = pd.read_csv('/Users/Diogenes/Documents/take_homes/BikeShare/data/weather_data.csv')
    else:
        path = input('Enter file path: ')
        stations = pd.read_csv(f'{path}station_data.csv')
        trips = pd.read_csv(f'{path}trip_data.csv',
                        parse_dates=['Start Date', 'End Date'], 
                        infer_datetime_format=True)
        weather = pd.read_csv(f'{path}weather_data.csv')

    return stations, trips, weather

def clean_trips_data_for_viz(df):
    '''
    A note included with the data indicates that several stations were
    relocated. Those include stations 23, 24, 49, 69 and 72, which
    became 85, 86, 87, 88 and 89, respectively. Subsequently, 89 later
    became 90, as well.

    Takes trips data frame as input and returns clean_trips, weekends
    and weekdays data frames, respectively.
    '''
    moved_stations=[23, 24, 49, 69, 72]
    new_stations1=[85, 86, 87, 88, 89]
    new_stations2=[90]

    replace_zip= list(zip(moved_stations, new_stations1))

    for s1, s2 in replace_zip:
        df.loc[df["Start Station"]==s1, "Start Station"]=s2

    df.loc[df["Start Station"]==89, "Start Station"]=90

    for s1, s2 in replace_zip:
        df.loc[df["End Station"]==s1, "End Station"]=s2

    df.loc[df["End Station"]==89, "End Station"]=90

    '''
    Additionally, it's valuable to have temporal measures like month,
    day of the week and hour of the day clearly delineated as columns
    '''

    df['month'] = df['Start Date'].dt.month
    df['day'] = df['Start Date'].dt.dayofweek
    df['hour'] = df['Start Date'].dt.hour

    clean_df = df.copy()
    weekends = clean_df[clean_df["Start Date"].dt.weekday >=5]
    weekdays = clean_df[clean_df["Start Date"].dt.weekday <5]

    return clean_df, weekends, weekdays

def list_for_heatmap(stat_df, trip_df):

    '''Takes stations and trips data frames, aggregates sum of trips per station
       and returns list of lat/long coordinates and trip count for each station
       and data frame to construct heatmap with timeseries data'''

    statlat = stat_df[['Id', 'Lat', 'Long']]
    tripslat = trip_df[['Start Date', 'Start Station', 'month', 'day', 'hour']].merge(statlat,
                                                                                left_on='Start Station',
                                                                                right_on='Id')
    tripslat['count'] = 1
    tripscount = pd.DataFrame(tripslat.groupby(['Start Station',
                                                'Lat',
                                                'Long'])
                            ['count'].sum().sort_values(ascending=False))
    lst = tripscount.groupby(['Lat', 'Long']).sum().reset_index().values.tolist()
    return lst, tripslat

if __name__ == '__main__':
    stations, trips, weather = retrieve_data()
    clean_df, weekends, weekdays = clean_trips_data_for_viz(trips)
    heat_lst, heat_df = list_for_heatmap(stations, trips)