import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mlp
import seaborn as sns
import clean

def make_compbars(df1, df2, title1, title2, order1, order2):
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

    fig.tight_layout()
    plt.show()

def make_groupbars(df, incr, title, xticklabels, xlabel):
    
    tdf = df.groupby([incr, 'Start Station']).size().reset_index(name='counts')
    tdfsrt = tdf.sort_values(['counts'], ascending=False)
    
    t5df = pd.DataFrame(columns=[incr, 'Start Station', 'counts'])
    
    for i in range(df[incr].max()+1):
        t5df = t5df.append(tdfsrt[tdfsrt[incr]==i][:5])

    fig, ax = plt.subplots(figsize=(12, 6))    
    sortedgroupedbar(ax, incr,'counts', "Start Station", xlabel, data=t5df)
    ax.set_title(title)
    ax.set_xticklabels(xticklabels)

    fig.tight_layout()
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

    
if __name__ == '__main__':
    stations, trips, weather = clean.retrieve_data()
    clean_df, weekends, weekdays = clean.clean_trips_data_for_viz(trips)
    
    dfs = [stations, trips, weather, clean_df, weekends, weekdays]

    titles = ['Top 5 Stations by Count of Trips',
              'Bottom 5 Stations by Count of Trips',
              'Top 5 Stations by Weekday Count of Trips',
              'Top 5 Stations by Weekend Count of Trips',
              'Top Weekday Stations by Trip Count',
              'Top Stations by Daily Trip Count',
              'Top Weekend Stations by Trip Count',
              'Top Stations by Monthly Trip Count']

    orders = [dfs[1]['Start Station'].value_counts().index[:5],
              dfs[1]['Start Station'].value_counts(ascending=True).index[:5],
              dfs[5]['Start Station'].value_counts().index[:5],
              dfs[4]['Start Station'].value_counts().index[:5]]

    increments = ['hour', 'day', 'month']

    months = []
    for i in range(trips.month.max()):
        months.append(f'{i + 1}')

    xticklabels = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                   ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                   ['Saturday', 'Sunday'],
                   months]

    xlabels = ['Day of Week', 'Weekend Day', 'Month of Year']
    
    # make_compbars(dfs[1], dfs[1], titles[0], titles[1], orders[0], orders[1])
    # make_compbars(dfs[5], dfs[4], titles[2], titles[3], orders[2], orders[3])
    make_groupbars(dfs[1], increments[2], titles[7], xticklabels[3], xlabels[2])