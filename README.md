# Student Performance Dashboard

An interactive dashboard built with Python and Streamlit to analyze student
performance across demographics, parental education, and test preparation.

## Project structure

```
student-performance-dashboard/
├── app.py                          # Streamlit dashboard (entry point)
├── requirements.txt
├── data/
│   └── study.csv                   # Cleaned dataset (1000 students)
├── notebooks/
│   ├── 01_data_cleaning.ipynb      # Load, clean, standardize, export
│   └── 02_exploratory_analysis.ipynb  # Score distributions & relationships
└── archive/                        # Earlier drafts, kept for reference
```

## Features

- Data cleaning: missing-value and duplicate checks, standardized column names
- Exploratory Data Analysis (EDA): distributions, boxplots, violin plots
- Interactive dashboard: subject/gender/parental-education filters
- Correlation analysis between Mathematics, Reading, and Writing scores
- Filtered-data CSV export from the dashboard

## Getting started

```bash
pip install -r requirements.txt
streamlit run app.py
```

To re-run the cleaning or EDA steps:

```bash
jupyter notebook notebooks/01_data_cleaning.ipynb
```

## Technologies

- Python, Pandas
- Matplotlib, Seaborn
- Streamlit
