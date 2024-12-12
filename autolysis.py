import os
import openai
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set OpenAI API base URL to the proxy
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"

# Set OpenAI API key to the proxy token from the environment variable
openai.api_key = os.getenv("AIPROXY_TOKEN")

def load_data(file_path):
    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback for non-UTF-8 files
        return pd.read_csv(file_path, encoding="latin1")

# Function to create charts (with limit on the number of charts)
def create_charts(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    # Filter only numeric columns for the correlation heatmap
    numeric_df = df.select_dtypes(include=["number"])

    chart_count = 0

    if not numeric_df.empty:
        # Generate a correlation heatmap (only one)
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig(f"{output_folder}/correlation_heatmap.png")
        plt.close()
        chart_count += 1

        # Generate only distribution plots for the first numeric column
        numeric_columns = numeric_df.columns
        if len(numeric_columns) > 0:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[numeric_columns[0]], kde=True)
            plt.title(f"Distribution of {numeric_columns[0]}")
            plt.savefig(f"{output_folder}/{numeric_columns[0]}_distribution.png")
            plt.close()
            chart_count += 1

        # Optionally generate another distribution plot for the second numeric column
        if len(numeric_columns) > 1 and chart_count < 3:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[numeric_columns[1]], kde=True)
            plt.title(f"Distribution of {numeric_columns[1]}")
            plt.savefig(f"{output_folder}/{numeric_columns[1]}_distribution.png")
            plt.close()
            chart_count += 1

# Function to generate story using OpenAI with gpt-4o-mini
def generate_story(df):
    # Create a summary of the dataframe
    summary = df.describe(include="all").to_string()

    # Prepare the prompt for the chat model
    prompt = f"""
    The following is a summary of a dataset:

    {summary}

    Write a short story explaining the key insights and trends from the data.
    """

    # Generate the story using gpt-4o-mini for chat-based completion
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Using gpt-4o-mini model for chat completion
        messages=[{"role": "system", "content": "You are a helpful data analyst."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()

# Function to write the README.md file
def write_readme(output_folder, story):
    readme_path = os.path.join(output_folder, "README.md")
    with open(readme_path, "w") as f:
        f.write("# Analysis Report\n\n")
        f.write(story)

# Main function to process each dataset
def main(csv_file, output_folder):
    print(f"Processing {csv_file}...")
    df = load_data(csv_file)
    create_charts(df, output_folder)
    story = generate_story(df)
    write_readme(output_folder, story)
    print(f"Finished processing {csv_file}. Results saved in {output_folder}")

# Paths to datasets
datasets = [
    ("C:\\Users\\Hario\\OneDrive\\Documents\\project\\automated_analysis_project\\media.csv", "media"),
    ("C:\\Users\\Hario\\OneDrive\\Documents\\project\\automated_analysis_project\\happiness.csv", "happiness"),
    ("C:\\Users\\Hario\\OneDrive\\Documents\\project\\automated_analysis_project\\goodreads.csv", "goodreads"),
]

# Process each dataset
for csv_file, folder in datasets:
    main(csv_file, folder)
