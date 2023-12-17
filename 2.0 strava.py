import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

#replace variables with values for your account
payload = {
    'client_id': "110632",
    'client_secret': 'Key_code',
    'refresh_token': '13ed9fdc2f0cf5a7326f6db2648648b9f636d96d',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset[0]["name"])
print(my_dataset[0]["map"]["summary_polyline"])

from pandas import json_normalize
activities = json_normalize(my_dataset)
activities.columns
print(my_dataset[1])

#Create new dataframe with only columns I care about
cols = ['name', 'upload_id', 'location_country', 'location_city', 'type', 'distance', 'moving_time',   
         'average_speed', 'max_speed','total_elevation_gain', 'average_heartrate',
         'start_date_local'
       ]

activities = activities[cols]

#Break date into start time and date
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date

activities.head(5)

activities['type'].value_counts()

import seaborn as sns

runs = activities.loc[activities['type'] == 'Run'] 
runs.head(5)

sns.set(style="ticks", context="talk")
sns.scatterplot(x='distance', y = 'average_speed', data = runs).set_title("Average Speed vs Distance")

sns.scatterplot(x='distance', y = 'max_speed', data = runs).set_title("Max Speed vs Distance")


import matplotlib.pyplot as plt
import numpy as np

#max speed over time
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.asarray(runs.start_date_local)
y = np.asarray(runs.max_speed)
ax.plot_date(x, y)
ax.set_title('Max Speed over Time')
fig.autofmt_xdate(rotation=45)
fig.tight_layout()
fig.show()

#average speed over time
fig = plt.figure()
ax1 = fig.add_subplot(111)
x = np.asarray(runs.start_date_local)
y = np.asarray(runs.average_speed)
ax1.plot_date(x, y)
ax1.set_title('Average Speed over Time')
fig.autofmt_xdate(rotation=45)
fig.tight_layout()
fig.show()

from datetime import datetime

import pandas as pd
# Define a conversion factor from miles to kilometers (1 mile = 1.60934 kilometers)
conversion_factor = 1.60934

# Convert the 'distance_miles' column to kilometers and store it in a new column
activities['speed_KM'] = activities['average_speed']*conversion_factor

# Print the updated DataFrame
print(df)

