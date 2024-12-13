import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import requests
import json
import openai

def analyze_data(df):
    """Analyze the data for summary statistics, missing values, and correlation matrix."""
    summary_stats = df.describe()
    missing_values = df.isnull().sum()
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr() if not numeric_df.empty else pd.DataFrame()
    return summary_stats, missing_values, corr_matrix

def detect_outliers(df):
    """Detect outliers using the IQR method."""
    df_numeric = df.select_dtypes(include=[np.number])
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df_numeric < (Q1 - 1.5 * IQR)) | (df_numeric > (Q3 + 1.5 * IQR))).sum()
    return outliers

def visualize_data(corr_matrix, outliers, df, output_dir):
    """Generate visualizations including correlation heatmap, outliers plot, and distribution plot."""
    heatmap_file, outliers_file, dist_plot_file = None, None, None

    if not corr_matrix.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Matrix')
        heatmap_file = os.path.join(output_dir, 'correlation_matrix.png')
        plt.savefig(heatmap_file)
        plt.close()

    if not outliers.empty and outliers.sum() > 0:
        plt.figure(figsize=(10, 6))
        outliers.plot(kind='bar', color='red')
        plt.title('Outliers Detection')
        plt.xlabel('Columns')
        plt.ylabel('Number of Outliers')
        outliers_file = os.path.join(output_dir, 'outliers.png')
        plt.savefig(outliers_file)
        plt.close()

    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[numeric_columns[0]], kde=True, color='blue', bins=30)
        plt.title(f'Distribution of {numeric_columns[0]}')
        dist_plot_file = os.path.join(output_dir, f'distribution_{numeric_columns[0]}.png')
        plt.savefig(dist_plot_file)
        plt.close()

    return heatmap_file, outliers_file, dist_plot_file

def create_readme(summary_stats, missing_values, corr_matrix, outliers, output_dir):
    """Generate a README.md file summarizing the data analysis."""
    readme_file = os.path.join(output_dir, 'README.md')
    try:
        with open(readme_file, 'w') as f:
            f.write("# Automated Data Analysis Report\n\n")
            f.write("## Introduction\n")
            f.write("This report provides an automated analysis of the dataset, including summary statistics, missing values, outlier detection, and visualizations.\n\n")

            f.write("## Summary Statistics\n")
            f.write(summary_stats.to_markdown() + "\n\n")

            f.write("## Missing Values\n")
            f.write(missing_values.to_markdown() + "\n\n")

            f.write("## Outliers\n")
            f.write(outliers.to_markdown() + "\n\n")

            if not corr_matrix.empty:
                f.write("## Correlation Matrix\n")
                f.write("![Correlation Matrix](correlation_matrix.png)\n\n")

            if outliers.sum() > 0:
                f.write("## Outliers Visualization\n")
                f.write("![Outliers](outliers.png)\n\n")

            f.write("## Distribution Plot\n")
            f.write("![Distribution](distribution_.png)\n\n")

        return readme_file
    except Exception as e:
        print(f"Error creating README.md: {e}")
        return None

def question_llm(prompt, context):
    """Generate a story using the OpenAI API."""
    try:
        token = os.environ.get("AIPROXY_TOKEN")
        if not token:
            return "API token not found. Please set the AIPROXY_TOKEN environment variable."

        api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt + "\n\n" + context}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {e}"

def main(csv_file):
    try:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print("Error reading the file. Ensure the file is in the correct format.")
        return

    summary_stats, missing_values, corr_matrix = analyze_data(df)
    outliers = detect_outliers(df)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    heatmap_file, outliers_file, dist_plot_file = visualize_data(corr_matrix, outliers, df, output_dir)

    story = question_llm("Generate a creative story based on this analysis:", context=f"Summary Stats: {summary_stats}\nMissing Values: {missing_values}\nCorrelation: {corr_matrix}")

    readme_file = create_readme(summary_stats, missing_values, corr_matrix, outliers, output_dir)
    if readme_file:
        with open(readme_file, 'a') as f:
            f.write("## Story\n")
            f.write(story + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <dataset_path>")
    else:
        main(sys.argv[1])
