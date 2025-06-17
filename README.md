# Gelbeseiten Web Scraper

A Python script for scraping business listings from [gelbeseiten.de](https://www.gelbeseiten.de) by industry and city using Selenium and BeautifulSoup.

## Features

- Headless Chrome browser scraping
- Extracts business name, address, and phone number
- Works with any industry and city available on Gelbeseiten

## Requirements

Install the dependencies using:

```bash
pip install -r requirements.txt
```

## How to run
```bash
python main.py "<industry>" "<city>"
```
```bash
python main.py "Bäckerei" "Berlin"
```
Example Output:
```bash
1. Bäckerei Müller
   Address: Hauptstraße 999, 10115 Berlin
   Phone: 0123456789
   Website: www.abc.com

