# Urban Housing Data Integration

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

**Project Description:**
Urban Housing Data Integration is a comprehensive data pipeline for extracting, cleaning, merging, and analyzing urban housing data from multiple sources (APIs, CSVs, Excel, PDFs, and web scraping). The project focuses on Florida housing trends, rental prices, and policy impacts.

**Topics:**
- Data Integration
- Housing Analytics
- Python Data Science
- Florida Housing Market
- Data Cleaning

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

## Quick Start
1. Clone the repository
2. Install required Python packages:
	```bash
	pip install -r requirements.txt
	```
3. Run the main data integration pipeline:
	```bash
	python Final_data.py
	```

## Usage Example
To run the full pipeline and generate the merged Florida housing dataset:
```bash
python Final_data.py
```
This will produce `Merger_cleaned_Prepared_data_for_Florida_by_group_9.csv` in the project folder.

## Setup
Install dependencies:
```bash
pip install pandas openpyxl tabula-py
```

## License
Specify your license here (e.g., MIT, Apache 2.0)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
