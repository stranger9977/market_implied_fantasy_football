from builtins import FileNotFoundError
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import re
from datetime import timedelta

api_key = os.environ.get("API_KEY")

# Get the current time in ISO8601 format
current_time_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")



# Regions and Markets
regions = ["us",'us2']
# check this out for avaialble markets https://the-odds-api.com/sports-odds-data/betting-markets.html
markets = [    'player_anytime_td']
    # 'player_pass_completions',
    # 'player_pass_interceptions',
    # 'player_pass_tds',
    # 'player_pass_yds',
    # 'player_reception_yds',
    # 'player_receptions',
    # 'player_rush_yds']

format = "american"

# Convert list to comma-separated string
regions_str = ",".join(regions)
markets_str = ",".join(markets)

# Date range for filtering events (for the current time)
commence_time_from = current_time_iso
commence_time_to = current_time_iso

# Step 1: Fetch event IDs
url_events = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/?apiKey={api_key}&regions={regions_str}&commenceTimeFrom={commence_time_from}&commenceTimeTo={commence_time_to}&oddsFormat={format}"
response_events = requests.get(url_events)
events_data = response_events.json()
# Extract event IDs
event_ids = [event['id'] for event in events_data]

# Initialize an empty list to store the fetched data
fetched_data = []

# Fetch odds for each event ID
for event_id in event_ids:
    url_odds = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{event_id}/odds/?apiKey={api_key}&regions={regions_str}&markets={markets_str}&oddsFormat={format}"
    response_odds = requests.get(url_odds)
    odds_data = response_odds.json()

    # Store the fetched data along with the event_id
    fetched_data.append({'event_id': event_id, 'odds_data': odds_data})

# Initialize an empty DataFrame
odds_df = pd.DataFrame()

# Iterate through the fetched data
for data in fetched_data:
    event_id = data['event_id']
    odds_data = data['odds_data']

    # Convert JSON to DataFrame
    temp_df = pd.json_normalize(odds_data, sep='_')

    # Add event_id as a level of multi-index
    temp_df['game_id'] = event_id

    # Extract bookmakers data into separate DataFrame and merge
    for bookmaker in odds_data['bookmakers']:
      if isinstance(bookmaker, dict):
          for market in bookmaker['markets']:
              bookmaker_df = pd.json_normalize(market['outcomes'], sep='_')
              bookmaker_df['bookmaker'] = bookmaker['key']
              bookmaker_df['last_update'] = market['last_update']
              bookmaker_df['market'] = market['key']

              # Check if 'point' exists and include it
              points = [outcome.get('point', None) for outcome in market['outcomes']]
              bookmaker_df['point'] = points

              # Concatenate with other relevant columns
              bookmaker_df = pd.concat([temp_df[['game_id', 'commence_time', 'home_team', 'away_team']], bookmaker_df], axis=1)

              # Append to the final DataFrame
              odds_df = pd.concat([odds_df, bookmaker_df])

# Convert 'price' and 'point' columns to numeric
odds_df['price'] = pd.to_numeric(odds_df['price'], errors='coerce')
odds_df['point'] = pd.to_numeric(odds_df['point'], errors='coerce')

# Forward fill the NaN values for these columns
odds_df[['game_id', 'commence_time', 'home_team', 'away_team']] = odds_df[['game_id', 'commence_time', 'home_team', 'away_team']].fillna(method='ffill')

# Assuming df is your DataFrame
# Define the list of markets you want to keep
markets_to_keep = [
    'player_anytime_td',
    'player_pass_completions',
    'player_pass_interceptions',
    'player_pass_tds',
    'player_pass_yds',
    'player_reception_yds',
    'player_receptions',
    'player_rush_yds'
]

# Filter the DataFrame to only include rows with the specified markets
odds_df = odds_df[odds_df['market'].isin(markets_to_keep)]
current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
odds_df['run_date'] = current_time

# Get the project root directory dynamically
project_root = os.environ.get("PROJECT_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
print(project_root)
# Create the full path for the CSV file
csv_file_path = os.path.join(project_root, 'market_implied_fantasy_football_tools', 'data', 'raw', 'odds.csv')

# Create the directory if it doesn't exist
directory = os.path.dirname(csv_file_path)
if not os.path.exists(directory):
    os.makedirs(directory)

most_recent_run_date = odds_df['run_date'].max()

print(f"The most recent run_date is: {most_recent_run_date}")
# Save the DataFrame to CSV
odds_df.to_csv(csv_file_path, index=False)


