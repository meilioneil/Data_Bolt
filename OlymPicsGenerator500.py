import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

# File paths
osPath = os.getcwd()
hosts = f'{os.getcwd()}\Data\Olympics\olympic_hosts.csv'
medals = f'{os.getcwd()}\Data\Olympics\olympic_medals.csv'
results = f'{os.getcwd()}\Data\Olympics\olympic_results.csv'
athletes = f'{os.getcwd()}\Data\Olympics\olympic_athletes.csv'
additional_data = f'{os.getcwd()}\Data\Olympics\Summer-Olympic-medals-1976-to-2008.csv'

# Load datasets
olympics_hosts = pd.read_csv(hosts)
olympics_athletes = pd.read_csv(athletes)
olympics_medals = pd.read_csv(medals)
olympics_results = pd.read_csv(results)
additional_olympics_info = pd.read_csv(additional_data, delimiter=",", encoding='latin1')

# Replace country codes and names
replacement_dict = {"URS": "RUS", "ROC": "RUS", "OAR": "RUS", "ORS": "RUS", "GDR": "GER", "FRG": "GER"}
additional_olympics_info["Country_Code"].replace(replacement_dict, inplace=True)
additional_olympics_info["Country"].replace({
    "Russian Federation": "Russia",
    "Soviet Union": "Russia",
    "Unified team": "Russia",
    "West Germany": "Germany",
    "East Germany": "Germany"
}, inplace=True)

# Replace country codes in olympics_medals and olympics_results
olympics_medals["country_3_letter_code"].replace(replacement_dict, inplace=True)
olympics_results["country_3_letter_code"].replace(replacement_dict, inplace=True)

# Merge datasets
olympics_results = pd.merge(olympics_hosts, olympics_medals, left_on='game_slug', right_on='slug_game', how='left')

# Filter for medals and summer games
Medals = olympics_results[(olympics_results['medal_type'].isin(['BRONZE', 'SILVER', 'GOLD'])) & (olympics_results['game_season'] == 'Summer')]

# Get unique sports
sports = Medals['discipline_title'].unique()

# Create the directory for saving plots
output_dir = 'olym-pics'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to sanitize filenames
def sanitize_filename(filename):
    return "".join([c if c.isalnum() or c in " _-" else "_" for c in filename])

for sport in sports:
    sport_medals = Medals[Medals['discipline_title'] == sport]

    # Aggregate total medals by country
    total_medals_by_country = sport_medals['country_3_letter_code'].value_counts().reset_index()
    total_medals_by_country.columns = ['country_3_letter_code', 'total_medals']

    # Get the top 10 countries by total medals
    top_10_countries = total_medals_by_country.head(10)['country_3_letter_code'].tolist()

    # Filter the medals data for only the top 10 countries
    top_10_medals = sport_medals[sport_medals['country_3_letter_code'].isin(top_10_countries)]

    # Aggregate medals by country and year for the top 10 countries
    medals_per_country_year = top_10_medals.groupby(['country_3_letter_code', 'game_year']).size().reset_index(name='medal_count')

    # Initialize plot
    plt.figure(figsize=(14, 8))

    # Create color map per country
    colors = sns.color_palette('tab10', len(top_10_countries))
    color_map = {country: colors[i] for i, country in enumerate(top_10_countries)}

    for country in medals_per_country_year['country_3_letter_code'].unique():
        country_data = medals_per_country_year[medals_per_country_year['country_3_letter_code'] == country]
        X = country_data['game_year'].values.reshape(-1, 1)
        y = country_data['medal_count'].values
        model = LinearRegression().fit(X, y)

        # Predict future values
        future_years = np.array([2024]).reshape(-1, 1)
        y_pred = model.predict(future_years)

        # Plot historical data (normal graph)
        plt.plot(country_data['game_year'], country_data['medal_count'], marker='o', label=country, color=color_map[country])

        # Draw Prediction line from the last historical value
        last_year = country_data['game_year'].values[-1]
        last_medal_count = country_data['medal_count'].values[-1]
        trendline_years = np.append(last_year, future_years).reshape(-1, 1)
        trendline_pred = np.append(last_medal_count, y_pred)
        plt.plot(trendline_years.flatten(), trendline_pred, linestyle='--', alpha=0.6, color=color_map[country])

    # Titles and labels
    plt.title(f'Medals Won by Top 10 Countries per Year in {sport} (with Predictions for 2024) [Summer Games]')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)

    # Save the plot
    plt.tight_layout()
    sanitized_sport = sanitize_filename(sport)
    output_path = os.path.join(output_dir, f'{sanitized_sport}_medals.png')
    plt.savefig(output_path)
    plt.close()

print(f'Plots saved in {output_dir} directory.')

