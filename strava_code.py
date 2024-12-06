import requests
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
from datetime import datetime
import seaborn as sns

# Load environment variables
load_dotenv()

# Setup Strava connection
auth_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"

# Replace variables with values for your account
payload = {
    'client_id': os.getenv('STRAVA_CLIENT_ID'),
    'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
    'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
    'grant_type': 'refresh_token',
    'f': 'json'
}

#request access token
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}

#create dataframe
my_dataset = requests.get(activities_url, headers=header, params=param).json()
activities = json_normalize(my_dataset)
activities.columns

activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date'] = activities['start_date_local'].dt.date
activities['start_month'] = activities['start_date_local'].dt.month
activities['start_month_name'] = activities['start_date_local'].dt.strftime('%B')
activities['start_year'] = activities['start_date_local'].dt.year

# Calculate average pace in minutes per kilometer
activities.loc[:, 'average_speed'] = 1 / (activities['average_speed'] * 0.06)
runs = activities.loc[activities['type'] == 'Run']

# Convert distance to kilometers
runs.loc[:, 'distance_km'] = runs['distance'] / 1000

# Set the Seaborn theme 
sns.set_theme(style="ticks", context="talk")

#create 4by4
pp_df = runs[['distance_km', 'total_elevation_gain', 'average_speed', 'average_heartrate']]
pair_plot = sns.pairplot(pp_df, diag_kind='kde', plot_kws={'alpha':0.6, 's':50, 'edgecolor':'k'}, 
                         diag_kws={'shade':True, 'color':'#4d4d4d'}, palette='Set2')

for ax in pair_plot.axes.flatten():
    if ax is not None:
        if ax.get_xlabel() in pp_df.columns and ax.get_ylabel() in pp_df.columns:
            sns.regplot(x=ax.get_xlabel(), y=ax.get_ylabel(), data=pp_df, scatter=False, ax=ax, line_kws={'color': 'red'})
        ax.set_xlabel(ax.get_xlabel().replace('_', ' ').title())
        ax.set_ylabel(ax.get_ylabel().replace('_', ' ').title())

pair_plot.fig.set_size_inches(14, 14)
plt.show()

# Create the boxplot 
fig, ax = plt.subplots()
sns.boxplot(x="start_year", y="distance_km", data=runs, palette="Set3", ax=ax)
ax.set_title("Distance per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Distance (KM)")
ax.grid(True, linestyle='--', alpha=0.6)
plt.gcf().set_size_inches(12, 8)
plt.tight_layout()
plt.show()

# create scatter plot with regression line
def plot_with_regression(ax, x, y, title, y_label, color):
    # Scatter plot
    ax.scatter(x, y, s=10, color=color, alpha=0.7)
    # Linear regression
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b, color=color, linewidth=2)
    # Titles and labels
    ax.set_title(title)
    ax.set_xlabel("Distance (KM)")
    ax.set_ylabel(y_label, labelpad=20) 
    ax.grid(True)

fig, axes = plt.subplots(1, 2)

# Average Speed vs Distance
plot_with_regression(
    axes[0],
    runs['distance_km'],
    runs['average_speed'],
    "Average Speed vs Distance (KM)",
    "Average Speed",
    color='blue'
)

# Max Speed vs Distance
plot_with_regression(
    axes[1],
    runs['distance_km'],
    runs['max_speed'],
    "Max Speed vs Distance (KM)",
    "Max Speed",
    color='green'
)
plt.tight_layout()
plt.show()