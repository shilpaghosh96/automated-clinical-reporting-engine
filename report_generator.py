import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def generate_visualizations(data, df):
    os.makedirs("report_assets", exist_ok=True)

    # Bar plot for depression counts
    depression_counts = data['consort_metrics']['depression_counts']
    plt.figure(figsize=(4, 4))
    sns.barplot(x=list(depression_counts.keys()), y=list(depression_counts.values()), palette='Set2')
    plt.title("Depression Counts")
    plt.ylabel("Number of Participants")
    plt.savefig("report_assets/depression_counts.png")
    plt.close()

    # Pie chart for gender
    gender_dist = data['consort_metrics']['gender_distribution']
    plt.figure(figsize=(4, 4))
    plt.pie(gender_dist.values(), labels=gender_dist.keys(), autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title("Gender Distribution")
    plt.savefig("report_assets/gender_pie.png")
    plt.close()

    # Sleep hours comparison
    insights = data['analytics_insights']
    plt.figure(figsize=(5, 4))
    sns.barplot(x=["Depressed", "Non-Depressed"],
                y=[insights['avg_sleep_hours_depressed'], insights['avg_sleep_hours_non_depressed']],
                palette="muted")
    plt.title("Average Sleep Hours")
    plt.ylabel("Hours")
    plt.savefig("report_assets/sleep_hours.png")
    plt.close()

def build_html_report(summary_text, data):
    html = f"""
    <html>
    <head>
        <title>Clinical CONSORT Summary Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; margin-top: 40px; }}
            img {{ max-width: 500px; margin: 20px 0; }}
            .section {{ margin-bottom: 40px; }}
            .metric-box {{ background: #ecf0f1; padding: 10px 20px; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>CONSORT-Style Clinical Trial Report</h1>

        <div class="section">
            <h2>📋 Narrative Summary</h2>
            <p>{summary_text}</p>
        </div>

        <div class="section">
            <h2>📊 Key Metrics</h2>
            <div class="metric-box">Total Participants: {data['consort_metrics']['total_participants']}</div>
            <div class="metric-box">Complete Records: {data['consort_metrics']['complete_records']}</div>
            <div class="metric-box">Depressed: {data['consort_metrics']['depression_counts']['Yes']}, Non-Depressed: {data['consort_metrics']['depression_counts']['No']}</div>
            <div class="metric-box">Avg Sleep (Depressed): {data['analytics_insights']['avg_sleep_hours_depressed']} hrs</div>
            <div class="metric-box">Avg CGPA (Depressed): {data['analytics_insights']['avg_cgpa_depressed']}</div>
        </div>

        <div class="section">
            <h2>📈 Visual Insights</h2>
            <img src="report_assets/depression_counts.png" alt="Depression Counts"/>
            <img src="report_assets/gender_pie.png" alt="Gender Distribution"/>
            <img src="report_assets/sleep_hours.png" alt="Sleep Hours"/>
        </div>
    </body>
    </html>
    """
    with open("consort_report.html", "w") as f:
        f.write(html)

    print("✅ HTML report saved as consort_report.html")

def generate_html_report():
    with open("summary_output.json") as f:
        data = json.load(f)

    with open("final_summary.txt") as f:
        summary_text = f.read()

    # You may also pass df if needed
    df = pd.read_csv("final_depression_dataset_1.csv")
    generate_visualizations(data, df)
    build_html_report(summary_text, data)

if __name__ == "__main__":
    generate_html_report()
