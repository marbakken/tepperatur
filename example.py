#tutorial from https://frost.met.no/python_example.html

#my client ID 3f43315b-e66c-488f-b443-36fde9880988
#my client secret b8598ab9-424f-4af5-bd35-28ca41ddafb7

#%%
import requests
import pandas as pd
#%%
# Insert your own client ID here
client_id = '3f43315b-e66c-488f-b443-36fde9880988'

# Define endpoint and parameters
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN18700',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2020-01-01/2021-01-01', #'2010-04-01/2010-04-10',
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
# These additional columns will be kept
columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
df2 = df[columns].copy()
# Convert the time value to something Python understands
df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

df.head()
df_main= df[df['index']==0]
print("Main sensor data:", df_main)

#%% 
df.hist(column='value', bins = 35)