import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Load datasets
results = pd.read_excel("NFL Schedule.xlsx")
status = pd.read_excel("NFL Player Status.xlsx")

# Filter status to only include rows where the player is out
status['out'] = np.where(status['Active_Inactive'] == "Out", 1, 0)

# Calculate the average snap rate for each category for each player who is out
status_in = status[status['out'] == 0]
# Calculate the average snap rate for each category for each player and season where 'out' is 0
player_avg = status_in.groupby(['name_abbr', 'Season'])[['Offense.Snap.Rate', 'Defense.Snap.Rate', 'Special.Teams.Snap.Rate']].mean().reset_index()

# Rename the columns
player_avg.rename(columns={
    'Offense.Snap.Rate': 'average_offense_snap_rate', 
    'Defense.Snap.Rate': 'average_defense_snap_rate', 
    'Special.Teams.Snap.Rate': 'average_special_teams_snap_rate'}, inplace=True)

# Merge this new data with status
status = pd.merge(status, player_avg, on=['name_abbr', 'Season'], how='left')

# Add Player Age at the start of the season
status['age'] = status.groupby(['Team', 'Season'])['Age_Start_Season'].transform('mean')
out = status.groupby(['Team', 'Season', 'Week', 'age','Offense.Snap.Rate','Defense.Snap.Rate','Special.Teams.Snap.Rate'])['out'].sum().reset_index()
out = out.sort_values(by=['Team', 'Season', 'Week'])


# Create a win-loss data at team-week-season level
winners = results[['Week', 'Season', 'Winner/tie']].rename(columns={'Winner/tie': 'Team'})
winners['win'] = 1
losers = results[['Week', 'Season', 'Loser/tie']].rename(columns={'Loser/tie': 'Team'})
losers['win'] = 0
win_loss = pd.concat([winners, losers]).sort_values(by=['Team', 'Season', 'Week'])

# Merge injuries & average age to win_loss data
finaldata = pd.merge(win_loss, out, on=['Team', 'Season', 'Week'], how='left')

# Account for relocated teams
relocations = {"Washington Redskins": "Washington Football Team",
               "St. Louis Rams": "Los Angeles Rams",
               "San Diego Chargers": "Los Angeles Chargers"}

finaldata['Team'] = finaldata['Team'].replace(relocations)

# Create win percentage by team-season & merge it to finaldata
team_season_wins = finaldata.replace(relocations).groupby(['Team', 'Season'])['win'].mean().reset_index(name='win_perc')
team_season_wins['lag_win_perc'] = team_season_wins.groupby(['Team'])['win_perc'].shift(1)
finaldata = pd.merge(finaldata, team_season_wins, on=['Team', 'Season'], how='left')

# Lowercase variable names
finaldata.columns = finaldata.columns.str.lower()

# Filter out 2015
finaldata = finaldata[finaldata['season'] != 2015]

finaldata.to_csv("final_data.csv", index=False)