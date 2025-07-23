from typing import Optional, Literal
from pydantic import BaseModel, ValidationError, conint, confloat
import pandas as pd
import numpy as np


class Participant(BaseModel):
    ID: int
    Name: str
    Gender: Literal["Male", "Female", "Other"]
    Age: conint(ge=10, le=100)
    City: str
    Working_Professional_or_Student: Literal["Working Professional", "Student"]
    Profession: Optional[str]
    Academic_Pressure: Optional[conint(ge=0, le=10)]
    Work_Pressure: Optional[conint(ge=0, le=10)]
    CGPA: Optional[confloat(ge=0, le=10)]
    Study_Satisfaction: Optional[conint(ge=0, le=5)]
    Job_Satisfaction: Optional[conint(ge=0, le=5)]
    Sleep_Duration: Optional[str]
    Dietary_Habits: Optional[Literal["Healthy", "Moderate", "Unhealthy"]]
    Degree: Optional[str]
    Have_you_ever_had_suicidal_thoughts: Literal["Yes", "No"]
    Work_Study_Hours: Optional[int]
    Financial_Stress: Optional[conint(ge=0, le=10)]
    Family_History_of_Mental_Illness: Literal["Yes", "No"]
    Depression: Literal["Yes", "No"]


REQUIRED_COLUMNS = [
    "ID", "Name", "Gender", "Age", "City", "Working_Professional_or_Student",
    "Profession", "Academic_Pressure", "Work_Pressure", "CGPA",
    "Study_Satisfaction", "Job_Satisfaction", "Sleep_Duration",
    "Dietary_Habits", "Degree", "Have_you_ever_had_suicidal_thoughts",
    "Work_Study_Hours", "Financial_Stress",
    "Family_History_of_Mental_Illness", "Depression"
]

def load_and_validate_csv(file_path: str) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Normalize column names (remove spaces, unify case)
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    # Check required columns
    if not set(REQUIRED_COLUMNS).issubset(df.columns):
        missing = set(REQUIRED_COLUMNS) - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Row validation using pydantic
    for idx, row in df.iterrows():
        row_dict = row.replace({np.nan: None}).to_dict()

        # Ensure that numeric fields with NaN values are set to None
        for column in ['Academic_Pressure', 'Work_Pressure', 'CGPA', 'Study_Satisfaction', 'Job_Satisfaction', 'Financial_Stress']:
            if pd.isna(row_dict[column]):
                row_dict[column] = None

        # Validate the row data using Pydantic
        try:
            Participant(**row_dict)
        except ValidationError as e:
            print(f"Validation error in row {idx + 1}:\n{e}")
            raise

    print(f"Successfully loaded and validated {len(df)} participants.")
    return df
