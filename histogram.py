#Get temperature histogram for several years

#%%
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#%%
# ---------- Insert your own client ID here!!
client_id = '3f43315b-e66c-488f-b443-36fde9880988'

# Define endpoint and parameters
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN18700', #Blindern 
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2013-01-01/2023-01-01' #-------Insert to and from date!!
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
df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

df.head()
df_main= df[df['index']==0]
print("Main sensor data:", df_main)

#%% Plot with one degree bins
temp_mean = df['value'].mean()
temp_min = df['value'].min()
temp_max = df['value'].max()
num_bins = np.ceil(temp_max-temp_min+1).astype(np.uint8)
temp_hist = df.hist(column='value', bins = num_bins)
plt.title('Temperature histogram ' + parameters['referencetime'])
plt.xlabel('Degrees')


#%% Compute percentile values
perc1=df['value'].quantile(0.01)
perc99=df['value'].quantile(0.99)
normal_range = perc99-perc1
print("1 percentile: (lower limit) ", perc1,"99 percentile (upper limit):", perc99)

counts,bins = np.histogram(df['value'],bins=num_bins,range=[perc1,perc99])
num_days = len(df['value'])

counts_precentage = counts/num_days*100
#%% Auto-generated Knitting colour histogram
num_colors = 16
df.hist(column='value', bins = num_colors,color = 'gray',range=[perc1,perc99],grid=False)
plt.title('Binned temperatures ' + parameters['referencetime'])
plt.xlabel('Degrees, 16 bins')
plt.show()
