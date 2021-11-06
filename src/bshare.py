import psycopg2
import numpy as np
import pandas as pd
import os

def connect_to_db():
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password='bzx59lth',
                            host="localhost",
                            port="5432")
    print(f'connected to {conn}')
    return conn

def query_db(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return results

def cmd_db(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    print(query)


def getStations(conn):
    query = '''SELECT distinct start_station from trips'''
    stations = query_db(conn, query)
    return stations

def makeStationTables(conn, Stations):
    for station in Stations:
        query = "CREATE TABLE trips_" + str(station[0]) + " AS TABLE trips WITH NO DATA"
        cmd_db(conn, query)
        #print(query)

def getTrafficStation(conn, Stations):
    for station in Stations:
        query = "insert into trips_" + str(station[0]) + " (select * from trips where start_station=" + str(station[0]) + " OR end_station =" + str(station[0]) + ") AS Temp "    
        print(query)


if __name__ == '__main__':
    conn = connect_to_db()
    #query = '''
    #    SELECT *
    #    FROM trips;
    #    '''
    #results = query_db(conn, query)
    stations = getStations(conn)
    print(stations)
    makeStationTables(conn, stations)
    getTrafficStation(conn, stations)
    #print(results)
    print('yay')