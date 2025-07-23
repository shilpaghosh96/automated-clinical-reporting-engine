from data_intake import load_and_validate_csv
from preprocess import clean_and_compute_metrics
from analytics import analyze_data
from summary_output import save_summary_to_json  # Save summary to JSON
import json
from flan_t5 import format_summary_prompt_from_json, run_flan_t5_on_prompt  # Updated import

def main():
    # Step 1: Load and validate the dataset
    df = load_and_validate_csv("final_depression_dataset_1.csv")
    
    # Step 2: Clean data and compute CONSORT-like metrics
    df, metrics = clean_and_compute_metrics(df)
    # Print cleaned data preview
    print("\n=== Cleaned Data Preview ===")
    print(df.head())
    
    # Step 3: Perform analysis and detect trends, dropouts, and outliers
    analysis = analyze_data(df)
    
    # Step 4: Save the summary (metrics + analysis) to a JSON file
    save_summary_to_json(metrics, analysis, 'summary_output.json')
    # Confirm JSON saving and summary generation
    print("\n=== Summary saved to summary_output.json ===")

    # Step 5: Generate a narrative summary using FLAN-T5
    prompt = format_summary_prompt_from_json("summary_output.json")  # Format prompt from JSON
    response = run_flan_t5_on_prompt(prompt)  # Generate the summary

    # Print the final generated summary
    print("\n=== FINAL SUMMARY ===\n")
    print(response)
    with open("final_summary.txt", "w") as f:
        f.write(response)

    # Print CONSORT-like metrics
    print("\n=== CONSORT-Like Metrics ===")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Print analytical insights
    print("\n=== Analytics Summary ===")
    for key, value in analysis.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
