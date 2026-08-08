import pandas as pd

df = pd.read_csv('C:/Users/hp/OneDrive/Desktop/ipl project/data/clean data/matches_clean.csv', parse_dates=['date'])
print('season_values=', sorted(df['season'].dropna().unique().tolist()))
print('2010_present=', 2010 in set(df['season'].dropna().unique().tolist()))

df2 = df.copy()
df2['season'] = pd.to_numeric(df2['season'], errors='coerce')
df2['season'] = df2['date'].dt.year
print('normalized_values=', sorted(df2['season'].dropna().unique().tolist()))
print('normalized_2010_present=', 2010 in set(df2['season'].dropna().unique().tolist()))
