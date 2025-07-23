# CONSORT Reporting Pipeline 

This project automates the generation of CONSORT-style clinical trial reports from structured CSV data. It takes raw participant-level data, cleans and analyzes it, computes key CONSORT metrics, generates a narrative summary using a language model (FLAN-T5), and visualizes the results—all in one streamlined pipeline.

---

## Pipeline Components

1. **Data Intake Agent**  
   - Loads and validates input CSV  
   - Uses `pandas`, `pyarrow`, `pydantic`, and `great_expectations`

2. **Preprocessing Agent**  
   - Cleans and computes metrics like dropout rates, treatment groups, and subgroup stats

3. **Analytics Agent**  
   - Identifies trends, dropouts, outliers  
   - Generates summary stats

4. **Narrative Generation Agent**  
   - Uses `google/flan-t5-small` to turn JSON analysis into a clinical summary

5. **Visualization Agent**  
   - Generates CONSORT-style diagrams and plots using `matplotlib`, `seaborn`, and `Graphviz`

6. **Report Generator**  
   - Outputs an HTML report combining narrative + visualizations

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/your-username/consort-summary-pipeline.git
cd consort-summary-pipeline

# (Optional) Create a virtual environment
conda create -n consort-pipeline python=3.10
conda activate consort-pipeline

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python main.py

# View final report
open consort_report.html   # On macOS
xdg-open consort_report.html  # On Linux (WSL or Ubuntu)
