import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

#replace variables with values for your account
payload = {
    'client_id': "110632",
    'client_secret': 'API_SECRET_KEY',
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


import pandas as pd
from pandas import json_normalize

activities = json_normalize(my_dataset)
activities.columns

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