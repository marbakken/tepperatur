#Get temperature histogram for several years

#%%
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#%%
# Insert your own client ID here
client_id = '3f43315b-e66c-488f-b443-36fde9880988'

print(today_str)
# Define endpoint and parameters
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN18700',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2012-01-01/2022-01-01'#'1961-01-01/1972-01-01', #-------Insert to and from date!!!
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
temp_mean = df['value'].mean()
temp_min = df['value'].min()
temp_max = df['value'].max()

#%% Degree bins
num_bins = np.ceil(temp_max-temp_min+1).astype(np.uint8)
temp_hist = df.hist(column='value', bins = num_bins)
plt.stem(temp_mean,400,'r')
plt.title('Temperature ' + parameters['referencetime'])
plt.xlabel('Degrees')


#%%
perc1=df['value'].quantile(0.01)
perc99=df['value'].quantile(0.99)
normal_range = perc99-perc1
bin_width = normal_range/16
print(perc1,perc99, bin_width)

counts,bins = np.histogram(df['value'],bins=num_bins,range=[perc1,perc99])
num_days = len(df['value'])

counts_precentage = counts/num_days*100
#%% Knitting colour histogram
num_bins = 16
df.hist(column='value', bins = num_bins,color = 'gray',range=[perc1,perc99],grid=False)
plt.stem(temp_mean,800,'black',markerfmt="")
plt.title('Temperature ' + parameters['referencetime'])
plt.xlabel('Degrees, 16 bins')
plt.show()

#%%