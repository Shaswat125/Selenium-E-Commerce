# 📦 ECommerceDataExtraction - Flipkart Product Scraper

Automates the extraction of mobile phone data from Flipkart using Selenium. Loads search/filter settings from a JSON config, applies filters like rating, storage, and camera specs, and writes the results to a local file.

---

## 🚀 Features

- 🔍 Dynamic filter application: ratings, storage, and camera
- 🧠 Modular codebase with reusable functions
- 📝 Extracted data saved to a human-readable `.txt` file
- 🧪 JSON-configurable XPath support
- 💡 Designed for easy extension and debugging

## 📂 Project Structure
├── ecommerce.py # Main scraping class
├── run_extraction.py # Runner script to execute the workflow
├── source_xpath.json # XPath and URL configuration file
├── PhoneData.txt # Output file for extracted data
└── util.py # Custom Selenium wrapper class

## 🛠 Requirements
- Python 3.7 or above
- Google Chrome (or Chromium)
- `selenium` package

### Install dependencies:
```bash
pip install selenium
