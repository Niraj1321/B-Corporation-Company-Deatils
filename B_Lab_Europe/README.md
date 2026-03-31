# B Lab Europe – Find a B Corp

## Project Overview
This project scrapes certified company directory details from the **B Lab Europe – Find a B Corp** platform.

The spider collects company information and exports the extracted data into both:

- `Find_A-B_Corp_Data.json`
- `Find_A-B_Corp_Data.xlsx`

## Files
- `data.py` — Scrapy spider file that crawls the certified directory, extracts company details, and saves the output in JSON and Excel formats.

## Requirements
Install the required Python packages before running the project:

```bash
pip install scrapy pandas openpyxl