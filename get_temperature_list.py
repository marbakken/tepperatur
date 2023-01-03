#tutorial from https://frost.met.no/python_example.html

#my client ID 3f43315b-e66c-488f-b443-36fde9880988
#my client secret b8598ab9-424f-4af5-bd35-28ca41ddafb7

#%%
from asyncio import AbstractEventLoop
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

from flask import Flask, request, render_template, session, redirect
#%%
'''
def get_temperature_data():
    # Insert your own client ID here
    client_id = '3f43315b-e66c-488f-b443-36fde9880988'

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    print(today_str)
    # Define endpoint and parameters
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': 'SN18700',
        'elements': 'mean(air_temperature P1D)',
        'referencetime': '2022-12-01/' + today_str #'2012-01-01/2022-01-01'#'1961-01-01/1972-01-01', #-------Insert to and from date!!!
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id,''))
    # Extract JSON data
    json = r.json()

    #%%
    # Check if the request worked, print out any errors
    if r.status_code == 200:
        data = json['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])

    #%%
    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame()
    for i in range(len(data)):
        row = pd.DataFrame(data[i]['observations'])
        row['referenceTime'] = data[i]['referenceTime']
        row['sourceId'] = data[i]['sourceId']
        df = df.append(row)

    df = df.reset_index()
    df.head()

    #%% Extract main values
    columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
    df2 = df[columns].copy()
    df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

    df.head()
    df_main= df[df['index']==0]
    print("Main sensor data:", df_main)

    #%%
    temperatures = df_main['value']
    color_number = np.uint8(np.round(temperatures/2)+5)
    color_number = color_number.clip(0,17)
    color_list = ['Sølv','Lyseblå', 'Jeansblå pelsull', 'Jeansblå tweed', 'Indigoblå', 'Turkis', 'Drageegg', 'Lysegrønn', 'Neongrønn', 'Sitrongul', 'Fnugg', 'Oker Finull', 'Oker Osloull', 'Oransje', 'Rosa-gul', 'Lys korall', 'Korall', 'Gull+korall']
    color_names = [color_list[n] for n in color_number]
    dates = df_main['referenceTime']
    table = pd.DataFrame({'Dato': dates, 'Gjennomsnittstemperatur': temperatures, 'Fargenummer': color_number, 'Fargenavn': color_names})
    # %%
    print(table)
    return table
'''
def get_temperature_data(client_id, start_date, end_date, station_code):

    # Define endpoint and parameters
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': station_code,
        'elements': elements,
        'referencetime': start_date + '/' + today_str #'2012-01-01/2022-01-01'#'1961-01-01/1972-01-01', #-------Insert to and from date!!!
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id,''))
    # Extract JSON data
    json = r.json()

    #%%
    # Check if the request worked, print out any errors
    if r.status_code == 200:
        data = json['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])

    #%%
    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame()
    for i in range(len(data)):
        row = pd.DataFrame(data[i]['observations'])
        row['referenceTime'] = data[i]['referenceTime']
        row['sourceId'] = data[i]['sourceId']
        df = df.append(row)

    df = df.reset_index()
    df.head()

    #%% Extract main values
    columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
    df2 = df[columns].copy()
    df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

    df.head()
    df_main= df[df['index']==0]
    print("Main sensor data:", df_main)
    return df_main

    #%%
def get_color_list(temperature_list,bin_width, min_value, num_colors, color_names = None):
    color_number = np.round(temperature_list/bin_width)-(min_value/bin_width)
    color_number_list = np.uint8(color_number.clip(0,num_colors+1))
    if color_names is None:
        color_name_list = []
    else:
        color_name_list = [color_names[n] for n in color_number_list]
    return color_number_list, color_name_list

if __name__ == '__main__':
    #--- Inputs ---
    #Weater data retrieval
    client_id = '3f43315b-e66c-488f-b443-36fde9880988' # Insert your own client ID here
    start_date = '2023-01-01'
    station_code = 'SN18700' #Blindern
    elements = 'mean(air_temperature P1D)'
    #Color definitions
    bin_size = 2 #degrees per colour
    min_value = -10 #minimum temperatures (for instance historical 1 percentile value)
    num_colors = 16 
    color_names = ['Sølv','Lyseblå', 'Jeansblå pelsull', 'Jeansblå tweed', 'Indigoblå', 'Turkis', 'Drageegg', 'Lysegrønn', 'Neongrønn', 'Sitrongul', 'Fnugg', 'Oker Finull', 'Oker Osloull', 'Oransje', 'Rosa-gul', 'Lys korall', 'Korall', 'Gull+korall']

    #--- Get temperatures and correponding colors
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    end_date = today_str
    temp_df =  get_temperature_data(client_id, start_date, end_date, station_code)
    temp_list = temp_df['value']
    color_number_list, color_name_list = get_color_list(temp_list,bin_size, min_value, num_colors, color_names)

    #--- Simple output: Print list with temperatures and colors
    dates = temp_df['referenceTime']
    table = pd.DataFrame({'Dato': dates, 'Gjennomsnittstemperatur': temp_list, 'Fargenummer': color_number_list, 'Fargenavn': color_name_list})
    print(table)
    

    

