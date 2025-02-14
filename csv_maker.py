#!/usr/bin/env python
# coding: utf-8

# All Imports

# In[2]:


from nba_api.stats.endpoints import PlayerDashboardByYearOverYear
from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerCareerStats
from nba_api.stats.endpoints import PlayByPlayV2 as pbp2
from nba_api.stats.endpoints import PlayerCareerStats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamGameLogs
from nba_api.stats.endpoints import TeamYearByYearStats
from datetime import datetime
import pandas as pd
import time
import re
import random
import requests
import os


# This is added onto all functions that require accessing the NBA API remotely. This way, if we receive a timeout, we can retry the API request without losing all progress made previously in the cell.

# In[3]:


# Retry Wrapper
def retry(func, retries=3):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        while attempts < retries:
            try: 
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                print(e)
            time.sleep(0.700)
            attempts += 1
    return retry_wrapper


# Get the pbp data for every game for a single season

# In[4]:


@retry
def getSingleGamePBP(game_id):
    full_single_game_pbp = pbp2(game_id=game_id)
    full_single_game_pbp = full_single_game_pbp.get_data_frames()[0]
    return full_single_game_pbp


# Gets pbp data for every season since 1996-1997 (pbp data first starts being tracked)

# In[6]:


@retry
def getFullSeasonPBP(season_string):

    print('Retrieving Game IDs for the ' + season_string + ' season at ' + str(datetime.now()))

     #Get all game_ids for a single season
    single_season_log = TeamGameLogs(season_nullable=season_string, season_type_nullable='Regular Season', league_id_nullable='00')
    single_season_logs = single_season_log.get_data_frames()[0]

    print('Finished retrieving Game IDs for the ' + season_string + ' season at ' + str(datetime.now()))

    # Eliminate duplicate games
    unique_games = single_season_logs.drop_duplicates(subset='GAME_ID')
    single_season_game_ids = unique_games['GAME_ID']

    single_season_pbp_df_list = []
    
    i = 0
    total = len(single_season_game_ids)

    for game_id in single_season_game_ids:
        i += 1
        print(f"Progress: {100 * i/total: .2f}%", end='\r')
        full_single_game_pbp = getSingleGamePBP(game_id)
        single_season_pbp_df_list.append(full_single_game_pbp)

    single_season_pbp_df = pd.concat(single_season_pbp_df_list)
    file_path = season_string + '.csv'
    single_season_pbp_df.to_csv(file_path, index=False)
    return single_season_pbp_df


# Get every game's play by play data from every season since the NBA API started keeping track of play by play data (1996-1997). Put this data into one csv so you can use it later and do not need to continuously retrieve every piece of play by play data.

# In[ ]:


# Loop through every game of every season and get all play by play data

all_time_pbp_df_list = []
season_string = ""

# Loop through 1996-1998 seasons
for i in range(96, 99):
    season_string = "19" + str(i) + "-" + str(i + 1)
    print('Retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))
    single_season_pbp_df = getFullSeasonPBP(season_string)
    all_time_pbp_df_list.append(single_season_pbp_df)
    print('Finished retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))

# Get 1999-2000 season
season_string = "1999-00"
print('Retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))
single_season_pbp_df = getFullSeasonPBP(season_string)
all_time_pbp_df_list.append(single_season_pbp_df)
print('Finished retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))


# Get 2000-2009 seasons
for i in range(0, 9):
    season_string = "200" + str(i) + "-0" + str(i + 1)
    print('Retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))
    single_season_pbp_df = getFullSeasonPBP(season_string)
    all_time_pbp_df_list.append(single_season_pbp_df)
    print('Finished retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))

# Get 2009-2010 season
season_string = "2009-10"
print('Retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))
single_season_pbp_df = getFullSeasonPBP(season_string)
all_time_pbp_df_list.append(single_season_pbp_df)
print('Finished retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))


# Get 2010-2019 seasons
for i in range(0, 9):
    season_string = "201" + str(i) + "-1" + str(i + 1)
    print('Retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))
    single_season_pbp_df = getFullSeasonPBP(season_string)
    all_time_pbp_df_list.append(single_season_pbp_df)
    print('Finished retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))

# Get 2019-2020 season
season_string = "2019-20"
print('Retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))
single_season_pbp_df = getFullSeasonPBP(season_string)
all_time_pbp_df_list.append(single_season_pbp_df)
print('Finished retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))


# Get 2020-2023 seasons
for i in range(0, 3):
    season_string = "202" + str(i) + "-2" + str(i + 1)
    print('Retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))
    single_season_pbp_df = getFullSeasonPBP(season_string)
    all_time_pbp_df_list.append(single_season_pbp_df)
    print('Finished retrieving Play by Play data for the ' + season_string + ' season at ' + str(datetime.now()))

# Save all play by play data from every season in one large csv file called 'allpbp.csv'
all_time_pbp_df = pd.concat(all_time_pbp_df_list)
file_path = 'allpbp.csv'
all_time_pbp_df.to_csv(file_path, index=False)


# Now that we have all the data in one csv, that file is extremely large (~2.3GB). We can eliminate many columns we do not need from the csv file and only keeps the ones we will use. This shrinks the file size down considerably (~1.7GB).

# In[ ]:


allpbp_file_path = '/Users/andyboulle/Downloads/School/Senior Year/MATH498R/Final/allpbp.csv'
pbp_df = pd.read_csv(allpbp_file_path)

columns_to_keep = ['GAME_ID', 'EVENTMSGTYPE', 'EVENTMSGACTIONTYPE', 'HOMEDESCRIPTION', 'NEUTRALDESCRIPTION', 'VISITORDESCRIPTION', 'PLAYER1_ID', 'PLAYER1_NAME', 'PLAYER1_TEAM_ID',
                   'PLAYER1_TEAM_CITY', 'PLAYER1_TEAM_NICKNAME', 'PLAYER1_TEAM_ABBREVIATION', 'PLAYER2_ID', 'PLAYER2_NAME', 'PLAYER2_TEAM_ID', 'PLAYER2_TEAM_CITY', 
                   'PLAYER2_TEAM_NICKNAME', 'PLAYER2_TEAM_ABBREVIATION']
pbp_df_condensed = pbp_df.filter(columns_to_keep)

# Write this condensed and filtered play by play dataframe to a csv called 'allpbp_filtered.csv'
file_path_filtered = 'allpbp_filtered.csv'
pbp_df_condensed.to_csv(file_path_filtered, index=False)


# Now that we have imported all the play by play data from every season, we can start to filter it so that it only includes the data we will need to analyze and-1 plays.

# In[7]:


allpbp_file_path = 'allpbp_filtered.csv'
pbp_df = pd.read_csv(allpbp_file_path)


# Filtering pbp data to only include made shots, fouls, and free throw attempts

# In[ ]:


all_time_shots_and_fouls_pbp = pbp_df[(pbp_df['EVENTMSGTYPE'] == 1) | (pbp_df['EVENTMSGTYPE'] == 6)
                                          | ((pbp_df['EVENTMSGTYPE'] == 3) & ((pbp_df['EVENTMSGACTIONTYPE'] == 10)
                                              | (pbp_df['EVENTMSGACTIONTYPE'] == 11) | (pbp_df['EVENTMSGACTIONTYPE'] == 13)))]
columns_to_keep = ['GAME_ID', 'EVENTMSGTYPE', 'EVENTMSGACTIONTYPE', 'HOMEDESCRIPTION', 'VISITORDESCRIPTION', 'PLAYER1_ID', 'PLAYER1_NAME', 'PLAYER1_TEAM_ABBREVIATION', 'PLAYER2_ID', 'PLAYER2_NAME', 'PLAYER2_TEAM_ABBREVIATION', ]
all_time_shots_and_fouls_pbp = all_time_shots_and_fouls_pbp.filter(columns_to_keep)
all_time_shots_and_fouls_pbp.head()


# Filtering previously filtered dataframe to only include and-1 plays (Made shot, shooting foul, same player taking free throw who made shot)

# In[ ]:


df = all_time_shots_and_fouls_pbp
and1_df = pd.DataFrame(columns=['Game_ID', 'Player_ID', 'Team', 'Opposing_Team', 'And_1s', 'Shooting_Fouls',
                                      'And_1s_2pt', 'And_1s_3pt', 'Shooting_Fouls_2pt', 'Shooting_Fouls_3pt'])

total = len(df)

for i in range(2, total):
    print(f"Progress: {100 * i/(total): .2f}%", end='\r')
    # detecting a shooting foul
    if df['EVENTMSGTYPE'].iloc[i - 1] == 6 and df['EVENTMSGACTIONTYPE'].iloc[i - 1] == 2:
        # detecting a 1 shot FT line visit
        if df['EVENTMSGTYPE'].iloc[i] == 3 and df['EVENTMSGACTIONTYPE'].iloc[i] == 10:
            # detecting a made basket
            # and that the free throw is taken by the same player who made the shot
            if df['EVENTMSGTYPE'].iloc[i - 2] == 1 and df['PLAYER1_ID'].iloc[i] == df['PLAYER1_ID'].iloc[i - 2]:
                # detecting a 3 pt shot
                if re.search('3PT', str(df['HOMEDESCRIPTION'].iloc[i - 2])) or re.search('3PT', str(df['VISITORDESCRIPTION'].iloc[i - 2])):
                    and1_df.loc[len(and1_df)] = [df['GAME_ID'].iloc[i], df['PLAYER1_ID'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i-1], 1, 1, 0, 1, 0, 1]
                else:
                    and1_df.loc[len(and1_df)] = [df['GAME_ID'].iloc[i], df['PLAYER1_ID'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i-1], 1, 1, 1, 0, 1, 0]
        # shooting foul, but no and 1
        else:
            if df['EVENTMSGTYPE'].iloc[i] == 3 and df['EVENTMSGACTIONTYPE'].iloc[i] == 13:
                and1_df.loc[len(and1_df)] = [df['GAME_ID'].iloc[i], df['PLAYER1_ID'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i-1], 0, 1, 0, 0, 0, 1]
            elif df['EVENTMSGTYPE'].iloc[i] == 3 and df['EVENTMSGACTIONTYPE'].iloc[i] == 11:
                and1_df.loc[len(and1_df)] = [df['GAME_ID'].iloc[i], df['PLAYER1_ID'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i], df['PLAYER1_TEAM_ABBREVIATION'].iloc[i-1], 0, 1, 0, 0, 1, 0]

# Save this dataframe of and-1 play by play data into a csv file called 'and1_df.csv'
file_path = 'and1_df.csv'
and1_df.to_csv(file_path, index=False)


# In[115]:


file_path = 'and1_df.csv'
and1_df = pd.read_csv(file_path)


# Adding season to each play in previous dataframe.

# In[ ]:


# Make a dictionary with the key being the year and the value
# being a list of Game IDs from that year. This will let us know
# what season each and 1 play took place

season_and_game_ids_dict = dict()

# Loop through 1996-1998 seasons
for i in range(96, 99):
    season_string = "19" + str(i) + "-" + str(i + 1)
    print('Retrieving Game IDs for the ' + season_string + ' season')
    result = TeamGameLogs(season_nullable=season_string, league_id_nullable='00')
    game_ids = result.get_data_frames()[0]['GAME_ID'].tolist()
    season_and_game_ids_dict[season_string] = game_ids
    
# Get 1999-2000 season
season_string = "1999-00"
print('Retrieving Game IDs for the ' + season_string + ' season')
result = TeamGameLogs(season_nullable=season_string, league_id_nullable='00')
game_ids = result.get_data_frames()[0]['GAME_ID'].tolist()
season_and_game_ids_dict[season_string] = game_ids


# Get 2000-2009 seasons
for i in range(0, 9):
    season_string = "200" + str(i) + "-0" + str(i + 1)
    print('Retrieving Game IDs for the ' + season_string + ' season')
    result = TeamGameLogs(season_nullable=season_string, league_id_nullable='00')
    game_ids = result.get_data_frames()[0]['GAME_ID'].tolist()
    season_and_game_ids_dict[season_string] = game_ids

# Get 2009-2010 season
season_string = "2009-10"
print('Retrieving Game IDs for the ' + season_string + ' season')
result = TeamGameLogs(season_nullable=season_string, league_id_nullable='00')
game_ids = result.get_data_frames()[0]['GAME_ID'].tolist()
season_and_game_ids_dict[season_string] = game_ids


# Get 2010-2019 seasons
for i in range(0, 9):
    season_string = "201" + str(i) + "-1" + str(i + 1)
    print('Retrieving Game IDs for the ' + season_string + ' season')
    result = TeamGameLogs(season_nullable=season_string, league_id_nullable='00')
    game_ids = result.get_data_frames()[0]['GAME_ID'].tolist()
    season_and_game_ids_dict[season_string] = game_ids

# Get 2019-2020 season
season_string = "2019-20"
print('Retrieving Game IDs for the ' + season_string + ' season')
result = TeamGameLogs(season_nullable=season_string, league_id_nullable='00')
game_ids = result.get_data_frames()[0]['GAME_ID'].tolist()
season_and_game_ids_dict[season_string] = game_ids


# Get 2020-2023 seasons
for i in range(0, 3):
    season_string = "202" + str(i) + "-2" + str(i + 1)
    print('Retrieving Game IDs for the ' + season_string + ' season')
    result = TeamGameLogs(season_nullable=season_string, league_id_nullable='00')
    game_ids = result.get_data_frames()[0]['GAME_ID'].tolist()
    season_and_game_ids_dict[season_string] = game_ids


# In[ ]:


# Add season each play took plcae in to its new column called 'Season'
and1_df['Season'] = None

total = len(and1_df)

for i in range(2, total):
    print(f"Progress: {100 * i/(total): .2f}%", end='\r')
    row = and1_df.iloc[i]
    game_id = row.Game_ID
    s = '00' + str(game_id)
    for key in season_and_game_ids_dict:
        if s in season_and_game_ids_dict[key]:
            and1_df.at[i, 'Season'] = key

# Save this new dataframe that includes season into a csv file called 'and1_df_w_season.csv
file_path = 'and1_df_w_season.csv'
and1_df.to_csv(file_path, index=False)


# In[176]:


file_path = 'and1_df_w_season.csv'
and1_df = pd.read_csv(file_path)


# This file is all the yearly stats from every team after the 1995-1996 season. This helps us calculate how effective and-1's are to winning.

# In[ ]:


# Get all team IDs from the nba
all_teams = teams.get_teams()
team_ids = [team['id'] for team in all_teams]

all_teams_yearly_stats = pd.DataFrame()

starting_season = '1995-96'

i = 0
total = len(team_ids)

for id in team_ids:
    i += 1
    print(f"Progress: {100 * i/total: .2f}%", end='\r')
    team_year_stats = TeamYearByYearStats(team_id=id, league_id='00', season_type_all_star='Regular Season', per_mode_simple='PerGame')
    team_year_stats = team_year_stats.get_data_frames()[0]
    filtered_stats = team_year_stats[team_year_stats['YEAR'] > starting_season]
    all_teams_yearly_stats = pd.concat([all_teams_yearly_stats, filtered_stats])

file_path = 'team_yearly_stats.csv'
all_teams_yearly_stats.to_csv(file_path, index=False)

