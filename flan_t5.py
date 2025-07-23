from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import json

def format_summary_prompt_from_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    metrics = data["consort_metrics"]
    insights = data["analytics_insights"]

    prompt = (
        "Generate a professional, clinical-style summary based on the following metrics and insights. "
        "Highlight differences between depressed and non-depressed participants, and include findings on CGPA, "
        "financial stress, academic pressure, suicidal thoughts, and sleep hours.\n\n"
        f"Total Participants: {metrics['total_participants']}\n"
        f"Complete Records: {metrics['complete_records']}\n"
        f"Gender: {metrics['gender_distribution']['Male']} Male, {metrics['gender_distribution']['Female']} Female\n"
        f"Profession: {metrics['profession_type_counts']['Student']} Students, {metrics['profession_type_counts']['Working Professional']} Working Professionals\n"
        f"Depression: {metrics['depression_counts']['Yes']} Yes / {metrics['depression_counts']['No']} No\n"
        f"Suicidal Thoughts: {metrics['suicidal_thoughts']['Yes']} Yes / {metrics['suicidal_thoughts']['No']} No\n"
        f"Average Work/Study Hours: {metrics['avg_work_study_hours']}\n"
        f"Average Financial Stress: {metrics['avg_financial_stress']}\n"
        f"CGPA (Depressed): {insights['avg_cgpa_depressed']}, CGPA (Non-Depressed): {insights['avg_cgpa_non_depressed']}\n"
        f"Academic Pressure (Depressed): {insights['avg_academic_pressure_depressed']}, (Non-Depressed): {insights['avg_academic_pressure_non_depressed']}\n"
        f"Sleep Hours (Depressed): {insights['avg_sleep_hours_depressed']}, (Non-Depressed): {insights['avg_sleep_hours_non_depressed']}\n"
    )

    return prompt

def run_flan_t5_on_prompt(prompt):
    model_id = "google/flan-t5-small"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)

    output_ids = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=2.0
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
