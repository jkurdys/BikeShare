# BikeShare EDA Project

## Objective: 
As part of a coding challenge I recently completed, I received the following assignment, which appears to be a variation on [an existing Kaggle challenge](https://www.kaggle.com/c/bike-sharing-demand). The project description reads as follows (**emphasis** added):
    
>Beachboys BikeShare is a bike share service provider where users can take and return bikes from any of 70 stations on their network. The company wants to leverage their data to better understand and, hopefully, optimize their operations. They are interested in exploring the potential for machine learning **to predict the number of bikes taken and returned to each station.**

>The eventual goal is to construct a model that can **predict the net rate of bike renting for a given station (net rate defined as trips ended minus trips started at the station for a given hour).** However, we would like you to just focus on doing the preliminary steps of this work. For this task we would like you to **focus on first doing the exploratory data analysis of the data provided.** Then we would like you to do the necessary data manipulations to create what would be your modeling data set. Finally, we would like you to do a short writeup about your next steps, and what modeling approaches you would examine first. Again, as you go through the work, bear in mind that your goal would be to **forecast net demand by hour by station** but you are not expected to build any models within the time limit.

Accordingly, for this phase of the project I will carry out the relevant EDA to identify the path for predicting net demand by hour by station.
    
## Data

The data contains three CSV files with information on the stations, trips-taken and weather affecting the bikeshare system.

- the stations data includes six columns of information to identify the station, station location and station capacity
- the trips data includes six columns to uniquely identify each of 350k trips, the start time and location of each trip and the type of user
- finally, weather data captures roughly a year of meteorological records from five stations spread throughout the city in 24 columns that include metrics like temperature, dew point, humidity, wind speed, cloud coverage, etc.

While I expect weather to significantly impact demand, I approached the problem as fundamentally a question of station location, usage by time of day and season for the relative stability of these features and because we can always layer the impact of weather on demand later once we understand how the flow of traffic from station to station, hour to hour and day to day affect demand.
Accordingly, I emphasized the features that helped trace the circulation of bike traffic between stations by hour, day, week and month in order to identify weather-independent usage patterns. Station identity and location were established with the unique station ID, name and coordinates from the stations table, whereas the datetime data and station ID from the trips table provided insight into the temporality of bike trips around the city.
    
    
## Exploratory Analysis

To begin, it helps to visualize the location of the stations in the BeachBoys BikeShare system. They cluster first in the northwest within the City of San Francisco and then moving southeast stretch out with less density from Redwood City through Palo Alto and Mountain View before forming a secondary cluster in San Jose.

![](/images/bike_station_map.html "BeachBoys BikeShare Station Map") 

Given the relative density of the stations, I expected to see most usage in San Francisco and San Jose to a lesser extent.
            
## Execution
- notebook walkthrough provides data preparation and code for wrangling into csv flat file
- link to EDA in Tableau included in notebook along with path to future integration with weather data
