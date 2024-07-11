import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px

# File paths <- make sure to change these in github!!
hosts = r'C:\Users\ASUS PC\Downloads\Olympics\olympic_hosts.csv'
medals = r'C:\Users\ASUS PC\Downloads\Olympics\olympic_medals.csv'
results = r'C:\Users\ASUS PC\Downloads\Olympics\olympic_results.csv'
athletes = r'C:\Users\ASUS PC\Downloads\Olympics\olympic_athletes.csv'
additional_data = r'C:\Users\ASUS PC\Downloads\Olympics\Summer-Olympic-medals-1976-to-2008.csv'

# Load datasets
olympics_hosts = pd.read_csv(hosts)
olympics_athletes = pd.read_csv(athletes)
olympics_medals = pd.read_csv(medals)
olympics_results = pd.read_csv(results)
additional_olympics_info = pd.read_csv(additional_data, delimiter=",", encoding='latin1')

# Replace country codes and names <- some countries have been combined
replacement_dict = {"URS": "RUS", "ROC": "RUS", "OAR": "RUS", "ORS": "RUS", "GDR": "GER", "FRG": "GER"}
additional_olympics_info["Country_Code"].replace(replacement_dict, inplace=True)
additional_olympics_info["Country"].replace({
    "Russian Federation": "Russia",
    "Soviet Union": "Russia",
    "Unified team": "Russia",
    "West Germany": "Germany",
    "East Germany": "Germany"
}, inplace=True)

# Replace country codes in olympics_medals and olympics_results <- from the above
olympics_medals["country_3_letter_code"].replace(replacement_dict, inplace=True)
olympics_results["country_3_letter_code"].replace(replacement_dict, inplace=True)

# Merge datasets <- just for ease
olympics_results = pd.merge(olympics_hosts, olympics_medals, left_on='game_slug', right_on='slug_game', how='left')

# Filter for medals and summer games
Medals = olympics_results[(olympics_results['medal_type'].isin(['BRONZE', 'SILVER', 'GOLD'])) & (olympics_results['game_season'] == 'Summer')]

# Aggregate total medals by country
total_medals_by_country = Medals['country_3_letter_code'].value_counts().reset_index()
total_medals_by_country.columns = ['country_3_letter_code', 'total_medals']

# Get the top 10 countries by total medals
top_10_countries = total_medals_by_country.head(10)['country_3_letter_code'].tolist()

# Filter the medals data for only the top 10 countries
top_10_medals = Medals[Medals['country_3_letter_code'].isin(top_10_countries)]

# Aggregate medals by country and year for the top 10 countries
medals_per_country_year = top_10_medals.groupby(['country_3_letter_code', 'game_year']).size().reset_index(name='medal_count')

# Create the plot
plt.figure(figsize=(14, 8))
for country in medals_per_country_year['country_3_letter_code'].unique():
    country_data = medals_per_country_year[medals_per_country_year['country_3_letter_code'] == country]
    plt.plot(country_data['game_year'], country_data['medal_count'], marker='o', label=country)

# Add titles and labels
plt.title('Medals Won by Top 10 Countries per Year')
plt.xlabel('Year')
plt.ylabel('Number of Medals')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Display the plot
plt.tight_layout()
plt.show()

