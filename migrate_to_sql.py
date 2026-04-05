# Τρέξτο αυτό σε ξεχωριστό αρχείο μία φορά
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/rocket_league.db')
seasonal_df = pd.read_csv('data/seasonal_master.csv')
rlcs_df = pd.read_csv('data/rlcs/games_by_players.csv')

seasonal_df.to_sql('seasonal_stats', conn, if_exists='replace', index=False)
rlcs_df.to_sql('rlcs_stats', conn, if_exists='replace', index=False)
conn.close()