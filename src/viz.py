import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib as mlp
import seaborn as sns
import folium
from folium.plugins import HeatMap, HeatMapWithTime
import io
from PIL import Image
import clean

plt.style.use('seaborn-whitegrid')

def make_compbars(df1, df2, title1, title2, order1, order2, save=False):
    fig, ax=plt.subplots(2, 1,  figsize=(12, 6))

    sns.countplot(x=df1["Start Station"],
                order= order1,
                ax=ax[0])
    ax[0].set_title(f"{title1}")
    ax[0].set_xlabel('Station')
    ax[0].set_ylabel('Trip Count')

    sns.countplot(x=df2["Start Station"],
                order= order2,
                ax=ax[1])
    ax[1].set_title(f"{title2}")
    ax[1].set_xlabel('Station')
    ax[1].set_ylabel('Trip Count')

    plt.tight_layout()
    if save:
        utitle1 = title1[:6].replace(' ', '_')
        utitle2 = title2[:6].replace(' ', '_', 2)
        plt.savefig('./images/'+utitle1+utitle2, dpi=125)
    
    else:
        plt.show()

def make_groupbars(df, incr, title, xticklabels, xlabel, save=False):
    
    tdf = df.groupby([incr, 'Start Station']).size().reset_index(name='counts')
    tdfsrt = tdf.sort_values(['counts'], ascending=False)
    
    t5df = pd.DataFrame(columns=[incr, 'Start Station', 'counts'])
    
    for i in range(df[incr].max()+1):
        t5df = t5df.append(tdfsrt[tdfsrt[incr]==i][:5])

    fig, ax = plt.subplots(figsize=(12, 6))    
    sortedgroupedbar(ax, incr,'counts', "Start Station", xlabel, data=t5df)
    ax.set_title(title)
    ax.set_xticklabels(xticklabels)

    plt.tight_layout()
    
    if save:
        title = title[:13].replace(' ', '_')
        plt.savefig('./images/'+ incr + '_' + title + 'group', dpi=125)
    else:
        plt.show()

def sortedgroupedbar(ax, x,y, groupby, xlabel, data=None, width=0.8, **kwargs):
    order = np.zeros(len(data))
    df = data.copy()
    
    for xi in np.unique(df[x].values):
        group = data[df[x] == xi]
        a = group[y].values
        b = sorted(np.arange(len(a)),key=lambda x:a[x],reverse=True)
        c = sorted(np.arange(len(a)),key=lambda x:b[x])
        order[data[x] == xi] = c   
    df["order"] = order
    u, df["ind"] = np.unique(df[x].values, return_inverse=True)
    step = width/len(np.unique(df[groupby].values))
    for xi,grp in df.groupby(groupby):
        ax.bar(grp["ind"]-width/2.+grp["order"]*step+step/2.,
               grp[y],width=step, label=xi, **kwargs)
    ax.legend(title=groupby)
    ax.set_xticks(np.arange(len(u)))

    ax.set_xlabel(xlabel)
    ax.set_ylabel('Trip Count')

def make_map(stat_df, title):
    stations_lst = stat_df.Id.to_list()
    coords_lst = list(zip(stat_df.Lat, stat_df.Long))
    names = stat_df.Name.to_list()
    station_names = list(zip(stations_lst, names))
    coords = list(zip(coords_lst, station_names))

    title_html = '''
                <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                '''.format(title)
    map = folium.Map(location=[37.56236, -122.150876], 
                            tiles='cartodbpositron',
                            zoom_start=10)
    map.get_root().html.add_child(folium.Element(title_html))

    for point, station in coords:
        marker = folium.Marker(location=point,
                                popup=station[1],
                                icon=folium.Icon(color='blue',icon='bicycle', prefix='fa'),
                                tooltip=station[0])
        marker.add_to(map)

    return map

def make_heatmap(lst, title, df= None, time= False):
    if time:
        df_hour_list = []

        for hour in df['hour'].sort_values().unique(): 
            df_hour_list.append(df.loc[df['hour'] == hour,
                                            ['Lat', 'Long', 'count']].groupby(['Lat', 'Long'])
                                .sum().reset_index().values.tolist())
        title_html = '''
                      <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                     '''.format(title)

        temp_heat_map = folium.Map(location=[37.56236, -122.150876], 
                                tiles='cartodbpositron',
                                zoom_start=10)
        start = dt.datetime(2021,1,1,0)
        end = dt.datetime(2021,1,1,23)
        daterange = pd.date_range(start=start,
                                  end=end,
                                  periods=24)

        time_index = [d.strftime("%I:%M %p") for d in daterange]

        HeatMapWithTime(df_hour_list,radius=11,
                        index=time_index,
                        gradient={0.1: 'blue', 0.5: 'lime', 0.7: 'orange', 1: 'red'}, 
                        min_opacity=0.4, 
                        max_opacity=0.8, 
                        use_local_extrema=True)\
                        .add_to(temp_heat_map)

        return temp_heat_map
    else:
        title_html = '''
                     <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                     '''.format(title)

        heat_map = folium.Map(location=[37.56236, -122.150876], 
                                tiles='cartodbpositron',
                                zoom_start=10)
        heat_map.get_root().html.add_child(folium.Element(title_html))
        HeatMap(data=lst, radius=12).add_to(heat_map)
        return heat_map

def group_plot(df, incr, agg_func, xticklabels,  xlabel, ylabel, title, save=False):
    '''
    Takes a dataframe, a list of columns to groupby, an aggregation function for the groups, 
    3 strings: label of x-axis, label of y-axis and title returns a line plot
    Plots the data with labels and title.
    '''
    
    group= getattr(df.groupby(incr), agg_func)()/1000
    ax= group.plot(figsize=(14,7), rot=70, fontsize=11)        
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(list(range(len(xticklabels))))
    ax.set_title(title)
    ax.set_xticklabels(xticklabels)
    if save:
        title = title[:12].replace(' ', '_')
        plt.savefig('./images/' + title + 'plot', dpi=125)
    else:
        plt.show()


if __name__ == '__main__':
    stations, trips, weather = clean.retrieve_data()
    clean_df, weekends, weekdays = clean.clean_trips_data_for_viz(trips)
    heat_lst, heat_df = clean.list_for_heatmap(stations, trips)
    
    dfs = [stations, trips, weather, clean_df, weekends, weekdays]

    titles = ['Top 5 Stations by Count of Trips',
              'Bottom 5 Stations by Count of Trips',
              'Top 5 Stations by Weekday Count of Trips',
              'Top 5 Stations by Weekend Count of Trips',
              'Top Weekday Stations by Trip Count',
              'Top Stations by Daily Trip Count',
              'Top Weekend Stations by Trip Count',
              'Top Stations by Monthly Trip Count',
              'Bay Area BikeShare Station Map',
              'Bay Area BikeShare Station Use by Time of Day',
              'Bay Area BikeShare Most Popular Stations',
              'Daily Trip Counts (Thousands)',
              'Monthly Trip Count (Thousands)',
              'Weekday Trip Count by Time of Day (Thousands)']

    orders = [dfs[1]['Start Station'].value_counts().index[:5],
              dfs[1]['Start Station'].value_counts(ascending=True).index[:5],
              dfs[5]['Start Station'].value_counts().index[:5],
              dfs[4]['Start Station'].value_counts().index[:5]]

    increments = ['hour', 'day', 'month']

    months = ['']
    for i in range(trips.month.max()):
        months.append(f'{i+1}')
        month = dt.datetime.strptime(months[i+1], '%m')
        months[i+1] = month.strftime('%b')

    hours = []
    for i in range(trips.hour.max()+1):
        hours.append(f'{i}:00')

    xticklabels = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                   ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
                   ['Saturday', 'Sunday'],
                   months,
                   hours]

    xlabels = ['Day of Week', 'Weekend Day', 'Month', 'Time of Day']
    
    # make_compbars(dfs[1], dfs[1], titles[0], titles[1], orders[0], orders[1])
    # make_compbars(dfs[5], dfs[4], titles[2], titles[3], orders[2], orders[3], save=True)
    # make_groupbars(dfs[1], increments[2], titles[7], xticklabels[3][1:], xlabels[2])
    # make_groupbars(dfs[1], increments[1], titles[5], xticklabels[1], xlabels[0])
    # stat_map.save('./images/bike_station_map.html')
    # heat_map = make_heatmap(heat_lst, titles[10], df= None, time= False)
    # heat_map.save('./images/bike_station_heatmap.html')
    # temp_heat_map = make_heatmap(heat_lst, titles[9], df= heat_df, time= True)
    # temp_heat_map.save('./images/bike_station_heatmap_wTime.html')
    # group_plot(dfs[1],increments[1], 'size', xticklabels[1], xlabels[0], 'Trip Count', titles[11])
    # group_plot(dfs[1],increments[0], 'size', xticklabels[4], xlabels[3], 'Trip Count', titles[13])
    # group_plot(dfs[1],increments[2], 'size', xticklabels[3], xlabels[2], 'Trip Count', titles[12])
