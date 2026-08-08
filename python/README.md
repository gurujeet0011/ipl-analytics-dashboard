# IPL Data Analytics Project

This project is a simple yet complete data analytics solution for the Indian Premier League. It takes raw IPL match and delivery data, cleans it, explores it, and presents it through charts and an interactive Streamlit dashboard.

The goal of this project is to make IPL data easier to understand for both beginners and people who want a quick story about teams, players, venues, and match trends.

## What this project includes

- Data cleaning and preparation for match-level and ball-by-ball IPL data
- Exploratory analysis using Python and visualization libraries
- A polished Streamlit dashboard for easy exploration
- Insights around team performance, player scoring, toss decisions, and venue usage

## Dataset

The project uses IPL match and delivery data from the 2008–2024 era.

- Source: Kaggle IPL complete dataset
- Main files used:
  - `matches.csv` → match-level information such as teams, venue, toss, winner, and result
  - `deliveries.csv` → ball-by-ball details for each match

## Project structure

```text
ipl project/
├── data/
│   ├── raw_data/
│   │   ├── matches.csv
│   │   └── deliveries.csv
│   └── clean data/
│       ├── matches_clean.csv
│       └── deliveries_clean.csv
├── python/
│   └── ipl_analysis.ipynb
├── streamlit_app/
│   └── app.py
├── requirements.txt
└── python/README.md
```

## Tools and libraries used

- Python
- pandas
- numpy
- matplotlib
- seaborn
- streamlit

## How to set up the project

1. Open the project folder in your terminal.
2. Create and activate a virtual environment if you want a clean setup.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to run the project

### 1. Run the notebook
Open and run the notebook in the `python` folder:

```text
python/ipl_analysis.ipynb
```

This notebook handles the data cleaning and analysis steps.

### 2. Run the Streamlit dashboard
From the project root, run:

```bash
streamlit run streamlit_app/app.py
```

This will open the dashboard in your browser.

## What you can explore in the dashboard

- Overview of completed matches and team performance
- Player stats such as top run scorers and wicket takers
- Venue analysis
- Trends such as toss decisions and run patterns
- Season-aware filters so teams and venues update based on the selected seasons
- Simple guidance messages when filters return no data or when the app needs a better selection
- Clear explanations for run-over charts and estimated total runs

## Notes

- The cleaned CSV files are already available in the `data/clean data` folder.
- This README is written in a simple, manually structured style so it feels more like a proper project guide than a generated template.

