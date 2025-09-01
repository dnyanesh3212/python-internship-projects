#!/usr/bin/env python3
"""
BBC News Web Scraper (Internship Project - Multi-Category with Browser Support)
-----------------------------------------------------------------------------
- Fetches BBC News headlines from multiple categories
- Categories: World, Sport, Technology, Business
- Optional keyword filtering
- Save results to CSV/TXT
- Simple text-based analysis
- Option to open a headline in web browser
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
from collections import Counter
import re
import xml.etree.ElementTree as ET   # fallback parser
import webbrowser  # ✅ for opening links

# BBC RSS feeds by category
RSS_FEEDS = {
    "1": ("World", "http://feeds.bbci.co.uk/news/world/rss.xml"),
    "2": ("Sport", "http://feeds.bbci.co.uk/sport/rss.xml"),
    "3": ("Technology", "http://feeds.bbci.co.uk/news/technology/rss.xml"),
    "4": ("Business", "http://feeds.bbci.co.uk/news/business/rss.xml"),
}

# ------------------ SCRAPER ------------------
def scrape_news(feed_url, keyword=None, limit=20):
    """Fetch headlines from BBC RSS feed (robust with fallback parsers)"""
    try:
        resp = requests.get(feed_url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print("[Error] Failed to fetch RSS:", e)
        return []

    results = []

    # --- Try BeautifulSoup with XML parser ---
    try:
        soup = BeautifulSoup(resp.content, "xml")
        items = soup.find_all("item", limit=limit)
        for item in items:
            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)
            if not link.startswith("http"):  # ✅ ensure full URL
                link = "https://www.bbc.com" + link
            if not keyword or keyword.lower() in title.lower():
                results.append((title, link))
    except Exception:
        # --- Fallback: use xml.etree (always available) ---
        root = ET.fromstring(resp.content)
        channel = root.find("channel")
        if channel is not None:
            for item in channel.findall("item")[:limit]:
                title = item.find("title").text
                link = item.find("link").text
                if not link.startswith("http"):  # ✅ ensure full URL
                    link = "https://www.bbc.com" + link
                if not keyword or keyword.lower() in title.lower():
                    results.append((title, link))

    return results

# ------------------ SAVE RESULTS ------------------
def save_results(results, filename, filetype="csv"):
    try:
        if filetype == "csv":
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Headline", "URL"])
                writer.writerows(results)
        elif filetype == "txt":
            with open(filename, "w", encoding="utf-8") as txtfile:
                for text, link in results:
                    txtfile.write(f"{text}\n{link}\n\n")
        print(f"✅ Saved results to {filename}")
    except Exception as e:
        print("[Error] Failed to save file:", e)

# ------------------ ANALYSIS ------------------
def analyze_headlines(results, keyword=None):
    texts = [text for text, _ in results]
    words = []
    for text in texts:
        words.extend(re.findall(r"\b\w+\b", text.lower()))

    counter = Counter(words)

    print("\n📊 Headline Analysis:")
    print(f"Total Headlines: {len(texts)}")
    if keyword:
        keyword_count = sum(keyword.lower() in t.lower() for t in texts)
        print(f"Keyword '{keyword}' appeared in {keyword_count} headlines.")
    print("Top 5 Common Words (excluding short words):")
    shown = 0
    for word, freq in counter.most_common(15):
        if len(word) > 3:
            print(f"  {word}: {freq}")
            shown += 1
        if shown >= 5:
            break
    print("-" * 40)

# ------------------ MAIN CLI ------------------
def main():
    print("="*50)
    print("   📰 BBC News Web Scraper (Internship CLI)   ")
    print("="*50)

    while True:  # ✅ keep program running until user exits
        # Ask category
        print("\nChoose a news category:")
        for key, (name, _) in RSS_FEEDS.items():
            print(f"{key}. {name}")
        print("0. Exit")
        choice = input("Enter choice (0-4): ").strip()

        if choice == "0":
            print("👋 Exiting. Goodbye!")
            sys.exit(0)

        if choice not in RSS_FEEDS:
            print("❌ Invalid choice. Try again.")
            continue

        category_name, feed_url = RSS_FEEDS[choice]

        keyword = input("Enter keyword to filter (press Enter for all): ").strip() or None
        results = scrape_news(feed_url, keyword)

        if not results:
            print("❌ No headlines found.")
            continue

        print(f"\nTop {len(results)} Headlines from BBC {category_name}{' (filtered)' if keyword else ''}:\n")
        for idx, (text, link) in enumerate(results, 1):
            print(f"{idx}. {text}\n   Link: {link}\n")

        # Option to save
        save_choice = input("Save results? (csv/txt/skip): ").strip().lower()
        if save_choice == "csv":
            save_results(results, f"bbc_{category_name.lower()}_headlines.csv", "csv")
        elif save_choice == "txt":
            save_results(results, f"bbc_{category_name.lower()}_headlines.txt", "txt")

        # Open in browser option
        open_choice = input("Open a headline in browser? (enter number or 'n'): ").strip().lower()
        if open_choice.isdigit():
            num = int(open_choice)
            if 1 <= num <= len(results):
                print(f"🌍 Opening: {results[num-1][1]}")
                webbrowser.open(results[num-1][1])
            else:
                print("❌ Invalid number.")

        analyze_headlines(results, keyword)
        print("\n✅ Done. Returning to main menu...\n")

if __name__ == "__main__":
    main()
