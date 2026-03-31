# B Corporation Data Scraper (Scrapy)

## Overview

This project is a **Scrapy-based web scraper** that extracts company data from the B Corporation API and saves it into:

* JSON file
* Excel file (.xlsx)

The scraper fetches paginated data from a Typesense-powered API and processes it into a structured dataset.

---

## Features

* Scrapes company data from B Corporation API
* Handles pagination automatically
* Cleans invalid Excel characters
* Converts timestamps into readable dates
* Saves output in:

  * JSON format
  * Excel format
* Removes duplicate records
* Error handling with logging

---

## Output Files

After running the scraper, the following files will be generated:

```
Find_A-B_Corp_Data.json
Find_A-B_Corp_Data.xlsx
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Niraj1321/B-Corporation-Company-Deatils.git



### 2. Install dependencies

```bash
pip install scrapy pandas openpyxl
```

---

## Usage

Run the spider using:

```bash
python data.py
```

OR (if inside Scrapy project):

```bash
scrapy crawl data
```

---

## How It Works

1. Sends a POST request to Typesense API
2. Retrieves company data in JSON format
3. Parses each record
4. Converts timestamps to readable dates
5. Stores results in memory
6. Handles pagination until all records are fetched
7. Saves final data into JSON and Excel

---

## Data Cleaning

* Removes illegal Excel characters
* Fills missing values with empty strings
* Converts column names to uppercase
* Removes duplicate rows

---

## Notes

* The API key is included in the script  consider moving it to environment variables for security.
* Large datasets may take time depending on pagination size.

---

## Error Handling

* Try-except blocks are used in:

  * Request handling
  * Parsing logic
  * File writing
* Logs errors using Scrapy logger

---

## Improvements (Optional)

* Add proxy support
* Implement retry middleware
* Store data in database (MongoDB / PostgreSQL)
* Add CLI arguments (page size, output path)
* Use environment variables for API keys

---

## License

This project is for educational and scraping purposes only. Ensure compliance with website terms of service before use.

---

## Author

Developed by Niraj

---

## Tip

If working with large datasets, consider using:

```python
df.to_csv("output.csv", index=False)
```

for faster exports compared to Excel.
