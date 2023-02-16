# import packages
import pandas as pd
import plotly.graph_objects as go
import nfl_data_py as nfl  # load data

df_2022 = nfl.import_pbp_data([2022])
df_players = nfl.import_rosters([2022])
df_teams = nfl.import_team_desc()

print(df_players.columns)
