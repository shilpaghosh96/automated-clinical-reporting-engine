# agents/analytics.py

import pandas as pd
import numpy as np
from scipy.stats import zscore

def map_sleep_to_hours(val):
    if pd.isna(val): return np.nan
    val = val.strip().lower()
    if 'less' in val: return 4
    if '5-6' in val: return 5.5
    if '7-8' in val: return 7.5
    if 'more' in val: return 9
    return np.nan

def analyze_data(df: pd.DataFrame) -> dict:
    analytics = {}

    # Normalize Sleep_Duration to numeric
    df['Sleep_Hours'] = df['Sleep_Duration'].apply(map_sleep_to_hours)

    # Grouped averages by Depression status
    depression_group = df[df['Depression'] == 'Yes']
    non_depression_group = df[df['Depression'] == 'No']

    features = [
        'CGPA', 'Work_Study_Hours', 'Financial_Stress', 'Academic_Pressure',
        'Work_Pressure', 'Study_Satisfaction', 'Job_Satisfaction', 'Sleep_Hours'
    ]

    for col in features:
        analytics[f'avg_{col.lower()}_depressed'] = round(depression_group[col].mean(), 2)
        analytics[f'avg_{col.lower()}_non_depressed'] = round(non_depression_group[col].mean(), 2)

    # Dropout definition: missing more than 5 fields
    df['missing_count'] = df.isna().sum(axis=1)
    df['is_dropout'] = df['missing_count'] > 5
    analytics['dropout_count'] = int(df['is_dropout'].sum())
    #analytics['dropout_participants'] = df[df['is_dropout']]['ID'].tolist()

    # High stress outliers (z > 2)
    #if 'Financial_Stress' in df.columns and df['Financial_Stress'].notna().sum() > 1:
     #   df['stress_zscore'] = zscore(df['Financial_Stress'].fillna(0))
      #  analytics['high_stress_flags'] = df[df['stress_zscore'] > 2]['ID'].tolist()
    #else:
    #    analytics['high_stress_flags'] = []

    return analytics
