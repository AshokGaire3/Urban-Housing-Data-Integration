# Urban Housing Data Integration

This project integrates, cleans, and analyzes urban housing data from multiple sources, including APIs, CSVs, Excel files, and PDFs. It is designed to help understand housing trends, rental prices, and policy impacts, with a focus on Florida.

## Features
- Data extraction from APIs, CSVs, Excel, and PDF files
- Data cleaning and merging
- Analysis of housing trends and rental prices
- Florida-specific housing data preparation

## File Overview
- `API_data.py`, `API_Housing_trends_data.py`: Scripts for API data extraction
- `CSV_data.py`, `CSV_rental.py`: Scripts for CSV data extraction
- `excel_data.py`: Script for Excel data extraction
- `pdf_data.py`: Script for PDF data extraction
- `merge_data.py`, `clean_merged_data.py`, `Final_data.py`: Data cleaning and merging scripts
- `cleaned_data.csv`, `florida_rental_data_cleaned.csv`, etc.: Output data files
- `housing_policy_fl.pdf`, `housing_policy.csv`: Policy documents

## Usage
1. Clone the repository
2. Install required Python packages (see below)
3. Run the relevant scripts for your analysis

## Setup
Install dependencies:
```bash
pip install pandas openpyxl tabula-py
```

## License
Specify your license here (e.g., MIT, Apache 2.0)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
