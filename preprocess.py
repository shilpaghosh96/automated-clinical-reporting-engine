import pandas as pd
import numpy as np

def clean_and_compute_metrics(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    # Standardize key text fields
    df['Gender'] = df['Gender'].str.strip().str.capitalize()
    df['Working_Professional_or_Student'] = df['Working_Professional_or_Student'].str.strip().str.title()
    df['Have_you_ever_had_suicidal_thoughts'] = df['Have_you_ever_had_suicidal_thoughts'].str.strip().str.title()
    df['Depression'] = df['Depression'].str.strip().str.title()

    # Normalize missing values
    df.replace(["", "NA", "NaN", "null", "None"], np.nan, inplace=True)

    # Define completion: if key fields are all present
    key_fields = ['Gender', 'Age', 'Working_Professional_or_Student', 'Depression']
    df['is_complete'] = df[key_fields].notna().all(axis=1)

    # Compute summary metrics
    metrics = {
        "total_participants": len(df),
        "complete_records": int(df['is_complete'].sum()),
        "incomplete_records": int((~df['is_complete']).sum()),
        "gender_counts": df['Gender'].value_counts(dropna=False).to_dict(),
        "profession_type_counts": df['Working_Professional_or_Student'].value_counts(dropna=False).to_dict(),
        "depression_counts": df['Depression'].value_counts(dropna=False).to_dict(),
        "suicidal_thoughts": df['Have_you_ever_had_suicidal_thoughts'].value_counts(dropna=False).to_dict(),
        "avg_work_study_hours": round(df['Work_Study_Hours'].mean(), 2),
        "avg_financial_stress": round(df['Financial_Stress'].mean(), 2),
    }

    return df, metrics
