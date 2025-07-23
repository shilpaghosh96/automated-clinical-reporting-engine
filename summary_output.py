import json

def format_for_gpt2(metrics: dict, analysis: dict) -> str:
    # Create a structured and conversational prompt
    lines = [
        "Write a detailed, coherent narrative summary based on the following clinical data:\n",
        "## CONSORT Metrics Summary:\n"
    ]

    # Make the metrics section more conversational
    lines.append(f"Participants: {metrics['total_participants']}")
    lines.append(f"Complete records: {metrics['complete_records']}")
    lines.append(f"Gender distribution: {metrics['gender_counts']['Male']} males, {metrics['gender_counts']['Female']} females")
    lines.append(f"Profession types: {metrics['profession_type_counts']['Working Professional']} working professionals, {metrics['profession_type_counts']['Student']} students")
    lines.append(f"Depression: {metrics['depression_counts']['Yes']} reported, {metrics['depression_counts']['No']} did not")
    lines.append(f"Suicidal thoughts: {metrics['suicidal_thoughts']['Yes']} reported, {metrics['suicidal_thoughts']['No']} did not")
    lines.append(f"Avg work/study hours: {metrics['avg_work_study_hours']}")
    lines.append(f"Avg financial stress: {metrics['avg_financial_stress']}")

    lines.append("\n## Analytics Insights:\n")
    # Analytics section: make it read like a summary
    lines.append(f"Avg CGPA (depressed): {analysis['avg_cgpa_depressed']}, (non-depressed): {analysis['avg_cgpa_non_depressed']}")
    lines.append(f"Avg work/study hours (depressed): {analysis['avg_work_study_hours_depressed']}, (non-depressed): {analysis['avg_work_study_hours_non_depressed']}")
    lines.append(f"Avg financial stress (depressed): {analysis['avg_financial_stress_depressed']}, (non-depressed): {analysis['avg_financial_stress_non_depressed']}")
    lines.append(f"Avg academic pressure (depressed): {analysis['avg_academic_pressure_depressed']}, (non-depressed): {analysis['avg_academic_pressure_non_depressed']}")
    lines.append(f"Avg sleep hours (depressed): {analysis['avg_sleep_hours_depressed']}, (non-depressed): {analysis['avg_sleep_hours_non_depressed']}")
    lines.append("No dropouts observed.")

    return "\n".join(lines)

def save_summary_to_json(metrics: dict, analysis: dict, filename: str):
    # Create a dictionary with structured data
    data = {
        "consort_metrics": {
            "total_participants": metrics['total_participants'],
            "complete_records": metrics['complete_records'],
            "gender_distribution": metrics['gender_counts'],
            "profession_type_counts": metrics['profession_type_counts'],
            "depression_counts": metrics['depression_counts'],
            "suicidal_thoughts": metrics['suicidal_thoughts'],
            "avg_work_study_hours": metrics['avg_work_study_hours'],
            "avg_financial_stress": metrics['avg_financial_stress']
        },
        "analytics_insights": {
            "avg_cgpa_depressed": analysis['avg_cgpa_depressed'],
            "avg_cgpa_non_depressed": analysis['avg_cgpa_non_depressed'],
            "avg_work_study_hours_depressed": analysis['avg_work_study_hours_depressed'],
            "avg_work_study_hours_non_depressed": analysis['avg_work_study_hours_non_depressed'],
            "avg_financial_stress_depressed": analysis['avg_financial_stress_depressed'],
            "avg_financial_stress_non_depressed": analysis['avg_financial_stress_non_depressed'],
            "avg_academic_pressure_depressed": analysis['avg_academic_pressure_depressed'],
            "avg_academic_pressure_non_depressed": analysis['avg_academic_pressure_non_depressed'],
            "avg_sleep_hours_depressed": analysis['avg_sleep_hours_depressed'],
            "avg_sleep_hours_non_depressed": analysis['avg_sleep_hours_non_depressed']
        },
        "conclusion": "Depression is linked to higher academic and financial stress, reduced work/study hours, and lower sleep quality. "
                      "It highlights the need for support systems to address mental health and academic pressures."
    }

    # Save the dictionary to a JSON file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Example of saving the summary to JSON
metrics = {
    'total_participants': 2556,
    'complete_records': 2556,
    'gender_counts': {'Male': 1333, 'Female': 1223},
    'profession_type_counts': {'Working Professional': 2054, 'Student': 502},
    'depression_counts': {'Yes': 455, 'No': 2101},
    'suicidal_thoughts': {'Yes': 1249, 'No': 1307},
    'avg_work_study_hours': 6.02,
    'avg_financial_stress': 2.97
}

analysis = {
    'avg_cgpa_depressed': 7.63,
    'avg_cgpa_non_depressed': 7.5,
    'avg_work_study_hours_depressed': 7.26,
    'avg_work_study_hours_non_depressed': 5.76,
    'avg_financial_stress_depressed': 3.47,
    'avg_financial_stress_non_depressed': 2.86,
    'avg_academic_pressure_depressed': 3.66,
    'avg_academic_pressure_non_depressed': 2.34,
    'avg_sleep_hours_depressed': 6.24,
    'avg_sleep_hours_non_depressed': 6.54
}

# Save to JSON
save_summary_to_json(metrics, analysis, 'summary_output.json')
