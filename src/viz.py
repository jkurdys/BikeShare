import matplotlib.pyplot as plt
import matplotlib as mlp
import seaborn as sns
import clean

def make_countplot(df):
    fig, ax=plt.subplots(figsize=(16, 5))
    sns.countplot(x=df["Start Station"], order= df['Start Station'].value_counts().index[:5], ax=ax)
    plt.show()
    
if __name__ == '__main__':
    stations, trips, weather = clean.retrieve_data()
    clean_df, weekends, weekdays = clean.clean_trips_data_for_viz(trips)
    make_countplot(trips)