import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px #change later
#from kaggle Olympic Games EDA
hosts = r'Olympics\olympic_hosts.csv'
medals = r'Olympics\olympic_medals.csv'
results = r'Olympics\olympic_results.csv'
athletes = r'Olympics\olympic_athletes.csv'
additional_data = r'C:\Users\ASUS PC\Downloads\Olympics\Summer-Olympic-medals-1976-to-2008.csv'
olympics_hosts = pd.read_csv(hosts)
olympics_athletes = pd.read_csv(athletes)
olympics_medals = pd.read_csv(medals)
olympics_results = pd.read_csv(results)
additional_olympics_info = pd.read_csv(additional_data,delimiter=",", encoding='latin1')
additional_olympics_info["Country_Code"].replace({"URS": "RUS",
                             "ROC": "RUS",
                             "OAR": "RUS",
                             "ORS": "RUS",
                             "GDR": "GER",
                             "FRG": "GER"}, inplace=True)
additional_olympics_info["Country"].replace({"Russian Federation": "Russia",
                        "Soviet Union": "Russia",
                        "Unified team": "Russia",
                        "West Germany": "Germany",
                        "East Germany": "Germany"}, inplace=True)
df_temp = additional_olympics_info[additional_olympics_info["Sport"].isin(['Aquatics','Archery', 'Athletics', 'Boxing', 'Canoe / Kayak',
                                                                       'Cycling', 'Equestrian', 'Fencing', 'Gymnastics', 'Judo', 'Modern Pentathlon',
                                                                        'Rowing', 'Sailing', 'Shooting', 'Weightlifting', 'Wrestling',
                                                                       'Table Tennis', 'Tennis', 'Badminton', 'Taekwondo', 'Triathlon'])]

# Group and aggregate the filtered data
df3 = df_temp.groupby(['Sport', 'Country', 'Country_Code', 'Year']).agg(Medal_size=('Medal', 'size')).sort_values('Medal_size', ascending=False).head(100).reset_index()

del df_temp


fig = px.histogram(df3, x='Country', y='Medal_size',hover_name='Country',  color='Sport', title='Top Medal winning nations and Sports')
fig.update_layout(legend_title_text='Sport')
