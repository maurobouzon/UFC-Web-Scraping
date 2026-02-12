🥊 UFC Web Scraping Project (UFCStats)

This project focuses on web scraping UFC fight and fighter statistics from the official public database UFCStats.com, using Python, Requests, BeautifulSoup and Pandas.

The goal is to build structured datasets that can later be used for data analysis, visualization, or even machine learning models to predict fight outcomes.

📌 Data Source

All data is scraped from:

UFCStats: http://ufcstats.com

🚀 Features

This project scrapes and builds multiple datasets, including:

✅ UFC Events Dataset

Scrapes all completed UFC events with:

Event name

Date

Location

Dataset output: events

✅ Fight Statistics per Event (TOTALS + SIGNIFICANT STRIKES)

For every event and every fight, the script scrapes round-by-round fight stats.

TOTALS Table

Includes:

Knockdowns (KD)

Significant strikes

Total strikes

Takedowns

Submission attempts

Reversals

Control time

Fight result metadata (method, referee, format, etc.)

Dataset output: TOTALS

SIGNIFICANT STRIKES Table

Includes detailed significant strike breakdown:

Head / Body / Leg

Distance / Clinch / Ground

Sig. strike % per round

Fight metadata

Dataset output: SIGNIFICANT_STRIKES

⚠️ Note: This script can take several minutes because it iterates through every event and fight page.

✅ Main Card / Fight Card Dataset

Scrapes fight card information from each UFC event, including:

Fighters

Weight class

Method

Round and time

Result (win/lose)

Dataset output: main_card_table

✅ Fighters Dataset (A-Z)

Scrapes the full UFC fighters list from A to Z (no lxml required).

Includes:

First name, Last name, Nickname

Height, Weight, Reach

Stance

Wins, Losses, Draws

Additionally, fighter data is cleaned and processed:

Height converted into centimeters

Weight converted into kilograms

W/L/D converted into numeric values

Dataset outputs:

fighters_raw

data_fighters_final

🛠️ Tech Stack

Python 🐍

Requests

BeautifulSoup4

Pandas

NumPy

📂 Output DataFrames

This project generates the following main DataFrames:

Dataset	Description
events	UFC completed events list
TOTALS	Round-by-round totals per fight
SIGNIFICANT_STRIKES	Round-by-round significant strikes breakdown
main_card_table	Fight card info per event
fighters_raw	Raw fighters dataset
data_fighters_final	Cleaned fighters dataset (height/weight processed)
⚙️ How to Run
1️⃣ Install dependencies
pip install requests beautifulsoup4 pandas numpy

2️⃣ Run the scripts

Each section of the code can be run independently depending on which dataset you want to generate.

⏳ Performance Notes

Scraping fight statistics requires looping through all events and all fights.

A small delay (time.sleep()) is included to avoid overloading the server.

📊 Possible Use Cases

UFC fight analytics dashboards

Fighter performance analysis

Predictive models for fight outcomes

Sports betting research

Data visualization projects

👤 Author

Mauro Bouzon
Data Scientist | Machine Learning & Analytics
📍 Montevideo, Uruguay
