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

def make_groupbars():
    pass
    
if __name__ == '__main__':
    stations, trips, weather = clean.retrieve_data()
    clean_df, weekends, weekdays = clean.clean_trips_data_for_viz(trips)
    
    dfs = [stations, trips, weather, clean_df, weekends, weekdays]

    titles = ['Top 5 Stations by Count of Trips',
              'Bottom 5 Stations by Count of Trips',
              'Top 5 Stations by Weekday Count of Trips',
              'Top 5 Stations by Weekend Count of Trips']

    orders = [dfs[1]['Start Station'].value_counts().index[:5],
              dfs[1]['Start Station'].value_counts(ascending=True).index[:5],
              dfs[5]['Start Station'].value_counts().index[:5],
              dfs[4]['Start Station'].value_counts().index[:5]]

    # make_compbars(dfs[1], dfs[1], titles[0], titles[1], orders[0], orders[1])
    make_compbars(dfs[5], dfs[4], titles[2], titles[3], orders[2], orders[3])