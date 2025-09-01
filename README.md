📂 Python Internship Projects – CLI Data Analysis Tools

This repository contains 3 Python CLI projects developed during my internship, designed to demonstrate data handling, API usage, web scraping, and basic data analysis.
These projects are internship submission–ready, while also serving as portfolio projects for a future Data Analyst / Data Scientist role.

📌 Projects Included
1️⃣ Weather CLI App 🌦️
Description:
A Command Line Interface (CLI) app that fetches real-time weather data using the OpenWeatherMap API.

Features:
Current weather (temperature, humidity, description, wind speed).
5-day forecast (every 3 hours) with simple CLI bar chart visualization.
Input validation (city name check).

Skills Shown:
API integration, JSON parsing, text-based visualization.

How to Run:
cd weather_cli
python weather_cli.py

2️⃣ E-commerce CLI System 🛒
Description:
A text-based e-commerce system that handles products, customers, and sales. Data is stored in CSV files.

Features:
Customer registration & login.
View products with low stock alerts.
Purchase products with coupon code discounts.
Restock products.
Sales report with text bar chart visualization.

Skills Shown:
CSV file handling, user management, sales reporting, business logic implementation.

How to Run:
cd ecommerce_cli
python ecommerce_cli.py

3️⃣ BBC News Web Scraper 📰
Description:
A CLI tool that scrapes BBC News RSS feeds across multiple categories and performs basic text analysis.

Features:
Choose category: World, Sport, Technology, Business.
Filter by keyword.
Save headlines to CSV/TXT.
Open headlines in browser directly from CLI.
Headline analysis: most frequent words, keyword matches.

Skills Shown:
Web scraping, text processing, word frequency analysis.

How to Run:
cd web_scraper
python web_scraper.py

⚙️ Installation

Clone the repository:
git clone https://github.com/YOUR_USERNAME/python-internship-projects.git
cd python-internship-projects


Install dependencies:
pip install -r requirements.txt

📦 Requirements
All projects share the same dependencies:

requests
beautifulsoup4
lxml

🎯 Skills Demonstrated
Python Programming
API Integration (OpenWeatherMap)
Web Scraping (BeautifulSoup + BBC RSS feeds)
Data Storage & File Handling (CSV, JSON)
Data Analysis & CLI Visualization

📜 License
Open-source, free to use for learning and portfolio purposes.
