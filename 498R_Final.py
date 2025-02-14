#!/usr/bin/env python
# coding: utf-8

# All Imports

# In[1]:


from nba_api.stats.static import players
from nba_api.stats.static import teams
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


# Setting Column and Row Display Options

# In[2]:


pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 999)


# Using and-1 dataframe to analyze data and group by player, team, season, etc

# In[7]:


and1_df = pd.read_csv('and1_df_w_season.csv')


# Analyze the top 50 players with the most total and-1's, 2pt and-1's, and 3pt and-1's since pbp data was tracked (1996-1997 season)

# In[8]:


# Group all and-1 plays by player only
player_and1_attempts = and1_df.groupby(['Player_ID']).sum(numeric_only=True)
player_and1_attempts.reset_index(inplace=True)


# In[ ]:


# Total and-1 leaders all time
all_time_and1_leaders_total = player_and1_attempts.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[False, True]).head(20)
all_time_and1_leaders_total['Player Name'] = all_time_and1_leaders_total['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_and1_leaders_total[['Player Name', 'And_1s', 'Shooting_Fouls', 'And_1s_2pt', 'And_1s_3pt']]


# In[ ]:


# 2pt and-1 leaders all time
all_time_and1_leaders_2pt = player_and1_attempts.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[False, True]).head(20)
all_time_and1_leaders_2pt['Player Name'] = all_time_and1_leaders_2pt['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_and1_leaders_2pt[['Player Name', 'And_1s_2pt', 'Shooting_Fouls', 'And_1s', 'And_1s_3pt']]


# In[ ]:


# 3pt and-1 leaders all time
all_time_and1_leaders_3pt = player_and1_attempts.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[False, True]).head(20)
all_time_and1_leaders_3pt['Player Name'] = all_time_and1_leaders_3pt['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_and1_leaders_3pt[['Player Name', 'And_1s_3pt', 'Shooting_Fouls', 'And_1s', 'And_1s_2pt']]


# Analyze the top 50 best individual seasons by a player in terms of total and-1's, 2pt and-1's, and 3pt and-1's

# In[265]:


# Group all and-1 plays by player and season
player_and1_attempts_by_season = and1_df.groupby(['Player_ID', 'Season']).sum(numeric_only=True)
player_and1_attempts_by_season.reset_index(inplace=True)


# In[ ]:


# Total and-1 leaders by season
season_and1_leaders_total = player_and1_attempts_by_season.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[False, True]).head(20)
season_and1_leaders_total['Player Name'] = season_and1_leaders_total['Player_ID'].apply(players.find_player_by_id).str['full_name']
season_and1_leaders_total[['Player Name', 'Season', 'And_1s', 'Shooting_Fouls', 'And_1s_2pt', 'And_1s_3pt']]


# In[ ]:


# 2pt and-1 leaders by season
season_and1_leaders_2pt = player_and1_attempts_by_season.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[False, True]).head(20)
season_and1_leaders_2pt['Player Name'] = season_and1_leaders_2pt['Player_ID'].apply(players.find_player_by_id).str['full_name']
season_and1_leaders_2pt[['Player Name', 'Season', 'And_1s_2pt', 'Shooting_Fouls', 'And_1s', 'And_1s_3pt']]


# In[ ]:


# 3pt and-1 leaders by season
season_and1_leaders_3pt = player_and1_attempts_by_season.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[False, True]).head(20)
season_and1_leaders_3pt['Player Name'] = season_and1_leaders_3pt['Player_ID'].apply(players.find_player_by_id).str['full_name']
season_and1_leaders_3pt[['Player Name', 'Season', 'And_1s_3pt', 'Shooting_Fouls', 'And_1s', 'And_1s_2pt']]


# Analyze the total percentage of shooting fouls result in an and-1. We will look at the percentage of total shooting fouls result in and-1's, the percentage of 2pt shooting fouls that result in and-1's, and the percentage of 3pt shooting fouls that result in and-1's.

# In[287]:


# Total and-1 percentage
all_time_total_and1_pct = and1_df['And_1s'].sum() / and1_df['Shooting_Fouls'].sum()
all_time_2pt_and1_pct = and1_df['And_1s_2pt'].sum() / and1_df['Shooting_Fouls_2pt'].sum()
all_time_3pt_and1_pct = and1_df['And_1s_3pt'].sum() / and1_df['Shooting_Fouls_3pt'].sum()

print('Shooting Fouls That Result in and And-1 Play: \t\t' + str((100 * all_time_total_and1_pct).round(2)) + '% (' + str(and1_df['And_1s'].sum()) + ' of ' + str(and1_df['Shooting_Fouls'].sum()) + ')')
print('2pt Shooting Fouls That Result in and And-1 Play: \t' + str((100 * all_time_2pt_and1_pct).round(2)) + '% (' + str(and1_df['And_1s_2pt'].sum()) + ' of ' + str(and1_df['Shooting_Fouls_2pt'].sum()) + ')')
print('3pt Shooting Fouls That Result in and And-1 Play: \t' + str((100 * all_time_3pt_and1_pct).round(2)) + '% (' + str(and1_df['And_1s_3pt'].sum()) + ' of ' + str(and1_df['Shooting_Fouls_3pt'].sum()) + ')')


# Analyze what players are the best and worst at drawing and-1's. This will be measure by their and-1 percentage. It is the number of and-1's they have drawn divided by the total number of shooting fouls they have drawn. We limit these to players who have scored 100 or more and-1 plays in their career because there are many who have just received a couple of shooting fouls and will probably have extremely high and-1 percentages, messing up the data.

# In[288]:


# Limit the number of players analyzed to players with 100 or more and-1 plays in their career
mask = player_and1_attempts['And_1s'] >= 100
player_and1_attempts_minimized = player_and1_attempts.loc[mask]


# In[ ]:


# Calculate and create and-1 percentage columns
player_and1_attempts_minimized['And_1_Percentage'] = player_and1_attempts['And_1s'] / player_and1_attempts['Shooting_Fouls']
player_and1_attempts_minimized['And_1_Percentage_2pt'] = player_and1_attempts['And_1s_2pt'] / player_and1_attempts['Shooting_Fouls_2pt']
player_and1_attempts_minimized['And_1_Percentage_3pt'] = player_and1_attempts['And_1s_3pt'] / player_and1_attempts['Shooting_Fouls_3pt']
player_and1_attempts_minimized


# In[ ]:


# Total and-1 pct leaders all time
all_time_total_and1_pct_leaders = player_and1_attempts_minimized.sort_values(by=['And_1_Percentage', 'Shooting_Fouls'], ascending=[False, True]).head(20)
all_time_total_and1_pct_leaders['Player Name'] = all_time_total_and1_pct_leaders['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_total_and1_pct_leaders[['Player Name', 'And_1s', 'Shooting_Fouls', 'And_1_Percentage']]


# In[ ]:


# Worst and-1 pcts all time
all_time_lowest_total_and1_pct = player_and1_attempts_minimized.sort_values(by=['And_1_Percentage', 'Shooting_Fouls'], ascending=[True, True]).head(20)
all_time_lowest_total_and1_pct['Player Name'] = all_time_lowest_total_and1_pct['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_lowest_total_and1_pct[['Player Name', 'And_1s', 'Shooting_Fouls', 'And_1_Percentage']]


# In[ ]:


# 2pt and-1 pct leaders all time
all_time_2pt_and1_pct_leaders = player_and1_attempts_minimized.sort_values(by=['And_1_Percentage_2pt', 'Shooting_Fouls'], ascending=[False, True]).head(20)
all_time_2pt_and1_pct_leaders['Player Name'] = all_time_2pt_and1_pct_leaders['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_2pt_and1_pct_leaders[['Player Name', 'And_1s', 'Shooting_Fouls', 'And_1_Percentage']]


# In[ ]:


# Worst 2pt and-1 pcts all time
all_time_lowest_2pt_and1_pct = player_and1_attempts_minimized.sort_values(by=['And_1_Percentage_2pt', 'Shooting_Fouls'], ascending=[True, True]).head(20)
all_time_lowest_2pt_and1_pct['Player Name'] = all_time_lowest_2pt_and1_pct['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_lowest_2pt_and1_pct[['Player Name', 'And_1s', 'Shooting_Fouls', 'And_1_Percentage']]


# In[393]:


# Limit the number of players analyzed to players with 3 or more and-1 plays on 3pt shots in their career
mask = player_and1_attempts['And_1s_3pt'] >= 3
player_and1_attempts_minimized = player_and1_attempts.loc[mask]


# In[ ]:


# Calculate and create and-1 percentage columns
player_and1_attempts_minimized['And_1_Percentage'] = player_and1_attempts['And_1s'] / player_and1_attempts['Shooting_Fouls']
player_and1_attempts_minimized['And_1_Percentage_2pt'] = player_and1_attempts['And_1s_2pt'] / player_and1_attempts['Shooting_Fouls_2pt']
player_and1_attempts_minimized['And_1_Percentage_3pt'] = player_and1_attempts['And_1s_3pt'] / player_and1_attempts['Shooting_Fouls_3pt']
player_and1_attempts_minimized


# In[ ]:


# 3pt and-1 pct leaders all time
all_time_3pt_and1_pct_leaders = player_and1_attempts_minimized.sort_values(by=['And_1_Percentage_3pt', 'Shooting_Fouls'], ascending=[False, True]).head(20)
all_time_3pt_and1_pct_leaders['Player Name'] = all_time_3pt_and1_pct_leaders['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_3pt_and1_pct_leaders[['Player Name', 'And_1s', 'Shooting_Fouls', 'And_1_Percentage']]


# In[ ]:


# Worst 3pt and-1 pcts all time
all_time_lowest_3pt_and1_pct = player_and1_attempts_minimized.sort_values(by=['And_1_Percentage_3pt', 'Shooting_Fouls'], ascending=[True, True]).head(20)
all_time_lowest_3pt_and1_pct['Player Name'] = all_time_lowest_3pt_and1_pct['Player_ID'].apply(players.find_player_by_id).str['full_name']
all_time_lowest_3pt_and1_pct[['Player Name', 'And_1s', 'Shooting_Fouls', 'And_1_Percentage']]


# Analyze the best teams historically at drawing and-1 fouls by total and-1's, 2pt and-1's, and 3pt and-1's

# In[ ]:


# Group all and-1 plays by team only
team_and1_attempts = and1_df.groupby(['Team']).sum()
team_and1_attempts.reset_index(inplace=True)
team_and1_attempts


# In[ ]:


# Total team and-1 leaders all time
team_all_time_and1_leaders_total = team_and1_attempts.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[False, True])
team_all_time_and1_leaders_total


# In[ ]:


# 2pt team and-1 leaders all time
team_all_time_and1_leaders_2pt = team_and1_attempts.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[False, True])
team_all_time_and1_leaders_2pt


# In[ ]:


# 3pt team and-1 leaders all time
team_all_time_and1_leaders_3pt = team_and1_attempts.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[False, True])
team_all_time_and1_leaders_3pt


# Analyze the 50 best and worst individual seasons by a team in terms of total and-1's, 2pt and-1's, and 3pt and-1's

# In[ ]:


# Group all and-1 plays by team and season
team_and1_attempts_by_season = and1_df.groupby(['Team', 'Season']).sum()
team_and1_attempts_by_season.reset_index(inplace=True)
team_and1_attempts_by_season


# In[ ]:


# Total team and-1 leaders by season
team_season_and1_leaders_total = team_and1_attempts_by_season.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_leaders_total


# In[ ]:


# Worst total team and-1's by season
team_season_and1_lowest_total = team_and1_attempts_by_season.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_lowest_total


# In[ ]:


# 2pt team and-1 leaders by season
team_season_and1_leaders_2pt = team_and1_attempts_by_season.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_leaders_2pt


# In[ ]:


# Worst 2pt team and-1's by season
team_season_and1_lowest_2pt = team_and1_attempts_by_season.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_lowest_2pt


# In[ ]:


# 3pt team and-1 leaders by season
team_season_and1_leaders_3pt = team_and1_attempts_by_season.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_leaders_3pt


# In[ ]:


# Worst 3pt team and-1's by season
team_season_and1_lowest_3pt = team_and1_attempts_by_season.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_lowest_3pt


# Calculate the difference between the average number of and-1 plays by teams during a given season, and each individual team's number of and-1 plays during that season. This will give us a scale for how well each team performed when it came to and-1 plays relative to other teams that season. We will call this stat and1+. 100 will be the baseline that a team had exactly the league average number of and-1 plays that season. The higher abover 100 it gets, the more and-1 plays compared to league average this team got that season, and the lower below 100 it gets, the less and-1 plays compared to league average this team got that season.

# In[ ]:


# Group all and-1 plays by season
season_and1_attempts = and1_df.groupby(['Season']).sum()
season_and1_attempts.reset_index(inplace=True)
season_and1_attempts


# In[218]:


# This function returns the number of teams in the league based on the given year. The Charlotte Bobcats were added in the 2003-04 season.
def numTeamsInTheLeague(season):
    if season == "1996-97" or season == "1997-98" or season == "1998-99" or season == "1999-00" or season == "2000-01" or season == "2001-02" or season == "2002-03" or season == "2003-04":
        return 29
    else:
        return 30


# In[219]:


# Apply the number of teams in the league to each season
season_and1_attempts['Num_Teams'] = season_and1_attempts['Season'].apply(numTeamsInTheLeague)

# Apply the avergage number of and-1 plays per team to each season
season_and1_attempts['Avg_And_1s'] = (season_and1_attempts['And_1s'] / season_and1_attempts['Num_Teams']).round(2)


# In[220]:


# Create a dictionary that uses season as the key and average number of and-1's per team as the value
# This makes it easier to compare when looking at the actual team performances each season
season_avg_and1s_dict = dict()

for index, row in season_and1_attempts.iterrows():
    season_avg_and1s_dict[row['Season']] = row['Avg_And_1s']


# In[221]:


team_and1_attempts_by_season['And_1+'] = (team_and1_attempts_by_season['And_1s'] /
                                           team_and1_attempts_by_season['Season'].apply(lambda x: season_avg_and1s_dict[x]) *
                                           100).round(2)


# Now that we have our And1+ variable created and set for each team each year, we can now determine relative to the rest of the teams in the league, which ones were the best and worst at drawing and-1 plays. Analyze the 50 best and worst individual season teams at drawing and-1's.

# In[ ]:


# Total team and1+ leaders by season
team_season_and1_leaders_total = team_and1_attempts_by_season.sort_values(by=['And_1+', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_leaders_total


# In[ ]:


# Worst total team and1+ by season
team_season_and1_lowest_total = team_and1_attempts_by_season.sort_values(by=['And_1+', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_lowest_total


# Now that we have each teams relative and-1 drawing success, we can use it to analyze other variables and determine how much effect it had on a team's success. (PPG Ranking, Win%, Off. Efficiency, etc.)

# In[224]:


# Make a dictionary connecting each abbreviation to a team id. This will allow us to retrieve
# yearly season data for each team by team id.

all_teams = teams.get_teams()
team_ids = [{'id': team['id'], 'name': team['abbreviation']} for team in all_teams]

team_ids_dict = dict()

possible_team_abbrevs = team_and1_attempts_by_season['Team'].unique()
current_team_abbrevs = [team['abbreviation'] for team in all_teams]

for value in possible_team_abbrevs:
    if value in current_team_abbrevs:
        team_ids_dict[value] = teams.find_team_by_abbreviation(value)['id']
    else: # Account for teams that have changed location
        if value == 'CHH':
            team_ids_dict[value] = teams.find_team_by_abbreviation('CHA')['id']
        elif value == 'NJN':
            team_ids_dict[value] = teams.find_team_by_abbreviation('BKN')['id']
        elif value == 'NOH':
            team_ids_dict[value] = teams.find_team_by_abbreviation('NOP')['id']
        elif value == 'NOK':
            team_ids_dict[value] = teams.find_team_by_abbreviation('NOP')['id']
        elif value == 'SEA':
            team_ids_dict[value] = teams.find_team_by_abbreviation('OKC')['id']
        elif value == 'VAN':
            team_ids_dict[value] = teams.find_team_by_abbreviation('MEM')['id']


# In[ ]:


# Set new column on dataframe to be team id
team_and1_attempts_by_season['Team_ID'] = (team_and1_attempts_by_season['Team'].apply(lambda x: team_ids_dict[x]))
team_and1_attempts_by_season


# In[226]:


# For each year's team, retrieve their yearly stats and set their 
# win percentage, points ranking, points per game, and free throws 
# attempted per game, then set the columns

# Retrieve the year by year stats of every team in the nba since 1996-1997
file_path = 'team_yearly_stats.csv'
nba_yearly_stats = pd.read_csv(file_path)

for index, row in team_and1_attempts_by_season.iterrows():
    team = team_ids_dict[row['Team']]
    season = row['Season']
    yearly_row = nba_yearly_stats.loc[(nba_yearly_stats['TEAM_ID'] == team) & (nba_yearly_stats['YEAR'] == season)]
    team_and1_attempts_by_season.at[index, 'PPG'] = yearly_row['PTS'].values[0]
    team_and1_attempts_by_season.at[index, 'Pts_Rank'] = yearly_row['PTS_RANK'].values[0]
    team_and1_attempts_by_season.at[index, 'Win_Pct'] = yearly_row['WIN_PCT'].values[0]
    team_and1_attempts_by_season.at[index, 'FTA_Per_Game'] = yearly_row['FTA'].values[0]


# Now that we have all the statistics we need, we can start to make visual representations of the relationships between and-1's and other variables. These graphs will make it easy to determine if a relationship actually exists and will demonstrate the value of drawing and-1's on offensive performance and winning.

# In[ ]:


# Plot and1+ and win percentage
and1_plus = team_and1_attempts_by_season['And_1+']
win_pct = team_and1_attempts_by_season['Win_Pct']

plt.scatter(and1_plus, win_pct)
plt.xlabel('And1+')
plt.ylabel('Win %')
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(and1_plus, win_pct)

print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_value**2)
print("p-value:", p_value)
print("Standard Error:", std_err)


# In[ ]:


# Plot and1+ and Points Rank
and1_plus = team_and1_attempts_by_season['And_1+']
pts_rank = team_and1_attempts_by_season['Pts_Rank']

plt.scatter(and1_plus, pts_rank)
plt.xlabel('And1+')
plt.ylabel('Point Rank')
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(and1_plus, pts_rank)

print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_value**2)
print("p-value:", p_value)
print("Standard Error:", std_err)


# In[ ]:


# Plot and1+ and Points Per Game
and1_plus = team_and1_attempts_by_season['And_1+']
ppg = team_and1_attempts_by_season['PPG']

plt.scatter(and1_plus, win_pct)
plt.xlabel('And1+')
plt.ylabel('Point Per Game')
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(and1_plus, ppg)

print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_value**2)
print("p-value:", p_value)
print("Standard Error:", std_err)


# In[ ]:


# Plot and1+ and Free Throws Attempted Per Game
and1_plus = team_and1_attempts_by_season['And_1+']
fta = team_and1_attempts_by_season['FTA_Per_Game']

plt.scatter(and1_plus, win_pct)
plt.xlabel('And1+')
plt.ylabel('Free Throws Attempted/Game')
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(and1_plus, fta)

print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_value**2)
print("p-value:", p_value)
print("Standard Error:", std_err)


# We have already explored the teams who draw the most and-1 plays and how that affects different offensive categories. But now lets explore the opposite and see which teams give up the most and-1 plays. We will examine all the same things that we looked at before except this time it will be reversed. Once we have all our date, we will now llok at how the number of and-1 plays given up affects win percentage.

# Analyze the teams historically that give up and-1 fouls by total and-1's, 2pt and-1's, and 3pt and-1's

# In[ ]:


# Group all and-1 plays by opposing team only
team_and1_commits = and1_df.groupby(['Opposing_Team']).sum()
team_and1_commits.reset_index(inplace=True)
team_and1_commits


# In[ ]:


# Total team and-1 committers all time
team_all_time_and1_committers_total = team_and1_commits.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[False, True])
team_all_time_and1_committers_total


# In[ ]:


# 2pt team and-1 committers all time
team_all_time_and1_committers_2pt = team_and1_commits.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[False, True])
team_all_time_and1_committers_2pt


# In[ ]:


# 3pt team and-1 committers all time
team_all_time_and1_committers_3pt = team_and1_commits.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[False, True])
team_all_time_and1_committers_3pt


# Analyze the 50 best and worst individual seasons by a team in terms of committed total and-1's, 2pt and-1's, and 3pt and-1's

# In[ ]:


# Group all and-1 plays by team and season
team_and1_commits_by_season = and1_df.groupby(['Opposing_Team', 'Season']).sum()
team_and1_commits_by_season.reset_index(inplace=True)
team_and1_commits_by_season


# In[ ]:


# Highest total team and-1 committers by season
team_season_and1_highest_committers_total = team_and1_commits_by_season.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_highest_committers_total


# In[ ]:


# Lowest total team and-1 committers by season
team_season_and1_lowest_committed_total = team_and1_commits_by_season.sort_values(by=['And_1s', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_lowest_committed_total


# In[ ]:


# Highest 2pt team and-1 committers by season
team_season_and1_highest_committers_2pt = team_and1_commits_by_season.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_highest_committers_2pt


# In[ ]:


# Lowest 2pt team and-1 committers by season
team_season_and1_lowest_committers_2pt = team_and1_commits_by_season.sort_values(by=['And_1s_2pt', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_lowest_committers_2pt


# In[ ]:


# Highest 3pt team and-1 committers by season
team_season_and1_highest_committers_3pt = team_and1_commits_by_season.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_highest_committers_3pt


# In[ ]:


# Lowest 3pt team and-1 committers by season
team_season_and1_lowest_committers_3pt = team_and1_commits_by_season.sort_values(by=['And_1s_3pt', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_lowest_committers_3pt


# Calculate the and1+ for each teams and-1's committed instead of drawn now. In this case, the value of and1+ is reversed. The higher a team's and1+, the less and-1's they committed and vice versa, meaning they were better at limiting their and-1's than the average team that year. 100 will be the baseline that a team committed exactly the league average number of and-1 fouls that season. The higher abover 100 it gets, the less and-1 plays compared to league average this team committed that season, and the lower below 100 it gets, the more and-1 plays compared to league average this team committed that season.

# In[ ]:


team_and1_commits_by_season['And_1+'] = (team_and1_commits_by_season['Season'].apply(lambda x: season_avg_and1s_dict[x]) / team_and1_commits_by_season['And_1s'] * 100).round(2)
team_and1_commits_by_season


# Now that we have our And1+ variable created and set for each team each year, we can now determine relative to the rest of the teams in the league, which ones were the best and worst at limiting their and-1 fouls. Analyze the 50 best and worst individual season teams at committing and-1's.

# In[ ]:


# Highest total team and1+ committers by season
team_season_and1_highest_committers_total = team_and1_commits_by_season.sort_values(by=['And_1+', 'Shooting_Fouls'], ascending=[True, True]).head(50)
team_season_and1_highest_committers_total


# In[ ]:


# Lowest total team and1+ committers by season
team_season_and1_lowest_committers_total = team_and1_commits_by_season.sort_values(by=['And_1+', 'Shooting_Fouls'], ascending=[False, True]).head(50)
team_season_and1_lowest_committers_total


# Now that we have each teams relative and-1 committing numbers, we can use it to analyze other variables and determine how much effect it had on a team's success. (Win%, fouls committed, etc.)

# In[ ]:


# Set new column on dataframe to be team id
team_and1_commits_by_season['Team_ID'] = (team_and1_commits_by_season['Opposing_Team'].apply(lambda x: team_ids_dict[x]))
team_and1_commits_by_season


# In[246]:


# For each year's team, retrieve their yearly stats and set their 
# win percentage and fouls committed, then set the columns

# Retrieve the year by year stats of every team in the nba since 1996-1997
file_path = 'team_yearly_stats.csv'
nba_yearly_stats = pd.read_csv(file_path)

for index, row in team_and1_commits_by_season.iterrows():
    team = team_ids_dict[row['Opposing_Team']]
    season = row['Season']
    yearly_row = nba_yearly_stats.loc[(nba_yearly_stats['TEAM_ID'] == team) & (nba_yearly_stats['YEAR'] == season)]
    team_and1_commits_by_season.at[index, 'Win_Pct'] = yearly_row['WIN_PCT'].values[0]
    team_and1_commits_by_season.at[index, 'PF_Per_Game'] = yearly_row['PF'].values[0]


# Now that we have all the statistics we need, we can start to make visual representations of the relationships between and-1's committed and other variables. These graphs will make it easy to determine if a relationship actually exists and will demonstrate the value of committing and-1's on defensive performance and winning.

# In[ ]:


# Plot and1+ and win percentage
and1_plus = team_and1_commits_by_season['And_1+']
win_pct = team_and1_commits_by_season['Win_Pct']

plt.scatter(and1_plus, win_pct)
plt.xlabel('And1+')
plt.ylabel('Win %')
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(and1_plus, win_pct)

print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_value**2)
print("p-value:", p_value)
print("Standard Error:", std_err)


# In[ ]:


# Plot and1+ and personal fouls
and1_plus = team_and1_commits_by_season['And_1+']
pf_per_game = team_and1_commits_by_season['PF_Per_Game']

plt.scatter(and1_plus, pf_per_game)
plt.xlabel('And1+')
plt.ylabel('Personal Fouls per Game')
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(and1_plus, pf_per_game)

print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_value**2)
print("p-value:", p_value)
print("Standard Error:", std_err)

