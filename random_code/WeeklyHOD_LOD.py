import yfinance as yf
import pandas as pd
from collections import Counter

# Download 5 years of QQQ daily data
data = yf.download('QQQ', period='5y', interval='1d')
data = data[['High', 'Low']]

# Add weekday column (Monday=0, ..., Friday=4)
data['Weekday'] = data.index.weekday

# Filter only trading days (exclude weekends)
data = data[data['Weekday'] < 5]

# Group by week
data['Year'] = data.index.year
data['Week'] = data.index.isocalendar().week

# Function to get high/low day of week for each week
def get_extreme_days(df):
    high_day = df['High'].idxmax()
    low_day = df['Low'].idxmin()
    return pd.Series({
        'HighDay': df.loc[high_day, 'Weekday'],
        'LowDay': df.loc[low_day, 'Weekday']
    })

weekly = data.groupby(['Year', 'Week']).apply(get_extreme_days).dropna()

# Only consider weeks with all 5 trading days
def full_week_filter(df):
    return len(df) == 5

full_weeks = data.groupby(['Year', 'Week']).filter(full_week_filter)
full_weeks_idx = set(full_weeks.groupby(['Year', 'Week']).groups.keys())
weekly = weekly.loc[weekly.index.isin(full_weeks_idx)]

# Count how often Tue (1) or Wed (2) is high/low day
high_counts = Counter(weekly['HighDay'])
low_counts = Counter(weekly['LowDay'])
total_weeks = len(weekly)

prob_tue_high = high_counts[1] / total_weeks
prob_wed_high = high_counts[2] / total_weeks
prob_tue_low = low_counts[1] / total_weeks
prob_wed_low = low_counts[2] / total_weeks

print(f"Probability Tuesday is highest of week: {prob_tue_high:.2%}")
print(f"Probability Wednesday is highest of week: {prob_wed_high:.2%}")
print(f"Probability Tuesday is lowest of week: {prob_tue_low:.2%}")
print(f"Probability Wednesday is lowest of week: {prob_wed_low:.2%}")