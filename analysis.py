# https://towardsdatascience.com/analyzing-and-plotting-nfl-data-with-nflfastpy-and-plotly-a170a09cad6

# https://github.com/venkatesannaveen/nfl-infographics

# import packages
import pandas as pd
import plotly.graph_objects as go
import nfl_data_py as nfl
# load data
df_2021 = nfl.import_pbp_data([2021])
df_players = nfl.import_rosters([2021])
df_teams = nfl.import_team_desc()

# print columns
df_2021.columns

# filter to regular season
df_2021 = df_2021[df_2021["season_type"] == "REG"]

# remove two point attempts
df_2021 = df_2021[df_2021["two_point_attempt"] == False]

# filter to pass plays
df_2021 = df_2021[df_2021["play_type"] == "pass"]

# join with the roster table to get player names
df_2021 = df_2021.merge(df_players[["player_id", "player_name"]], left_on="passer_player_id", right_on="player_id")

# join with team table to get team color for plot
df_2021 = df_2021.merge(df_teams[["team_abbr", "team_color"]], left_on="posteam", right_on="team_abbr")

# get total passing yards and touchdowns by week
df_agg = (
    df_2021.groupby(["player_name", "team_abbr", "team_color", "week"], as_index=False)
    .agg({"passing_yards": "sum", "pass_touchdown": "sum"})
)

df_agg[df_agg["player_name"] == "Josh Allen"]

fig = go.Figure()
for name, values in df_agg.groupby("player_name"):
    if values["passing_yards"].sum() > 1500:
        fig.add_trace(
            go.Scatter(
                x=values["week"], 
                y=values["passing_yards"].cumsum(), 
                name=name, 
                mode="markers+lines", 
                line_color=values.iloc[0].team_color,
                hovertemplate=f"<b>{name}</b><br>%{{y}} yds through week %{{x}}<extra></extra>"
            )
        )
    
fig.update_layout(
    font_family="Averta, sans-serif",
    hoverlabel_font_family="Averta, sans-serif",
    xaxis_title_text="Week",
    xaxis_title_font_size=18,
    xaxis_tickfont_size=16,
    yaxis_title_text="Passing Yards",
    yaxis_title_font_size=18,
    yaxis_tickfont_size=16,
    hoverlabel_font_size=16,
    legend_font_size=16,
    height=1000,
    width=1000
)
    
fig.show()