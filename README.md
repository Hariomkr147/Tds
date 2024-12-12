
# Automated Data Analysis Project

## Project Overview

This project automates the process of analyzing datasets. It includes multiple stages such as:
1. **Loading datasets**: Loading `.csv` files.
2. **Data visualization**: Automatically generating visualizations like correlation heatmaps and distribution plots.
3. **Textual insights generation**: Using OpenAI's GPT-4o-mini model to generate insightful summaries based on the dataset’s structure and statistics.
4. **Structured report generation**: Saving the results in folders, including the visualizations and a markdown `README.md` file, which contains an overview of the analysis and insights.

The goal of this project is to enable non-experts to understand their datasets quickly by providing both visual and textual summaries, thereby improving data comprehension and decision-making.

### Key Features:
- **Automatic Data Processing**: Loads, analyzes, and visualizes data from `.csv` files.
- **Data Visualization**:
  - Generates correlation heatmaps for numeric features.
  - Produces distribution plots for key numeric columns.
- **Natural Language Insights**: Generates a summary of the dataset, explaining trends, distributions, and key features.
- **Markdown Report**: Outputs all results in well-organized directories with a comprehensive `README.md` file summarizing the analysis.

## Project Structure

### Root Directory:
The root of the repository contains all the scripts and CSV files needed for the analysis.

```bash
├── happiness.csv                # Dataset containing happiness-related data
├── goodreads.csv                # Dataset containing Goodreads book data
├── media.csv                    # Dataset containing media-related data
├── happiness/                   # Folder containing outputs for the happiness dataset
│   ├── README.md                # Narrative report for happiness dataset
│   ├── correlation_heatmap.png   # Correlation heatmap for happiness data
│   ├── happiness_distribution.png  # Distribution plot for happiness data
├── goodreads/                   # Folder containing outputs for the Goodreads dataset
│   ├── README.md                # Narrative report for Goodreads dataset
│   ├── correlation_heatmap.png   # Correlation heatmap for Goodreads data
│   ├── goodreads_distribution.png # Distribution plot for Goodreads data
├── media/                       # Folder containing outputs for media dataset
│   ├── README.md                # Narrative report for media dataset
│   ├── correlation_heatmap.png   # Correlation heatmap for media data
│   ├── media_distribution.png    # Distribution plot for media data
├── main.py                       # Main script that orchestrates data analysis
├── requirements.txt             # List of dependencies for the project
└── LICENSE                      # License file for the project
```

### Generated Outputs:
Each dataset is processed individually. The results for each dataset are saved in separate folders (`happiness`, `goodreads`, `media`). Each folder includes:
1. A `README.md` file containing the generated insights and a summary of the analysis.
2. Generated visualizations (charts) such as:
   - **Correlation heatmap**: A visual representation of the relationships between numeric columns in the dataset.
   - **Distribution plot**: A histogram and kernel density estimation (KDE) plot of a chosen numeric column to understand its distribution.

## Requirements

Before running the project, make sure you have Python 3.x installed on your system, along with the following dependencies:

- **openai**: For interacting with the OpenAI API to generate textual insights.
- **pandas**: For handling and analyzing datasets in `.csv` format.
- **seaborn**: For creating advanced data visualizations like heatmaps and distribution plots.
- **matplotlib**: For plotting and saving charts.

### Installing Dependencies
You can install all required dependencies at once by running:

```bash
pip install -r requirements.txt
```

Alternatively, you can install the dependencies individually by running:

```bash
pip install openai pandas seaborn matplotlib
```

## Usage

### Running the Script

1. **Set Up Your OpenAI API Key**:  
   Make sure to set your OpenAI API key as an environment variable. This is essential for using GPT-4o-mini to generate insights.

   In your terminal, run:

   ```bash
   export AIPROXY_TOKEN="your-api-key-here"
   ```

2. **Run the Analysis**:  
   To process the datasets, run the main script (`main.py`). This script will automatically:
   - Load the specified datasets from `.csv` files.
   - Create visualizations like heatmaps and distribution plots.
   - Generate a narrative summary of the data using the OpenAI API.
   - Save all results in the corresponding folder for each dataset.

   Run the script using:

   ```bash
   python main.py
   ```

   The script will process the datasets and generate the following outputs:
   - A folder for each dataset (e.g., `happiness`, `goodreads`, `media`).
   - Inside each folder, you will find:
     - A `README.md` file containing the analysis report.
     - PNG files for the generated visualizations.

### Example of Generated Output:

For example, in the `happiness` dataset folder, you will find:
- `README.md`: Contains the story generated by GPT-4o-mini, which explains the key trends and insights from the happiness dataset.
- `correlation_heatmap.png`: Shows a correlation heatmap of numeric columns in the dataset, helping to visualize relationships between variables.
- `happiness_distribution.png`: Shows the distribution of the first numeric column, helping understand its spread and trends.

## How It Works

### 1. Data Loading:
- **Function**: `load_data(file_path)`
- The function loads the CSV file into a Pandas DataFrame, first attempting to use UTF-8 encoding, and if that fails, falling back to Latin1 encoding to handle different file formats.

### 2. Data Visualization:
- **Function**: `create_charts(df, output_folder)`
- This function generates two types of charts:
  1. **Correlation heatmap** for numeric columns, showing how the variables relate to one another.
  2. **Distribution plot** for a numeric column, showing how the values of that column are distributed (via histogram and KDE).
- The charts are saved as PNG images in the specified output folder.

### 3. Insights Generation with OpenAI:
- **Function**: `generate_story(df)`
- The function generates a summary of the dataset by sending a prompt to OpenAI’s GPT-4o-mini model. It uses the `describe()` method from Pandas to generate statistical descriptions of the dataset and provides those insights as input to the model.
- The model then generates a narrative that explains the key insights and trends in the data.

### 4. Writing the Report:
- **Function**: `write_readme(output_folder, story)`
- The narrative generated by the OpenAI model is written into a `README.md` file, which provides a comprehensive summary of the dataset, including an explanation of the visualizations and trends.

### Example Workflow:
1. **Data Loading**: A dataset (`happiness.csv`) is loaded and processed.
2. **Visualization Generation**: A correlation heatmap and distribution plot are generated for the dataset and saved.
3. **Insights Generation**: The statistical summary of the dataset is sent to OpenAI’s GPT-4o-mini model to generate a human-readable story.
4. **Output**: The results, including the markdown report and visualizations, are saved in a folder (`happiness/`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI API**: Used for generating insightful narratives based on dataset descriptions.
- **Seaborn**: Used for creating advanced visualizations, including correlation heatmaps.
- **Matplotlib**: Used for generating and saving static visualizations.
- **Pandas**: Used for data manipulation and analysis.

