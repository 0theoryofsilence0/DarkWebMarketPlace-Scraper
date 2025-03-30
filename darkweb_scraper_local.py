import os
import json
import spacy
from bs4 import BeautifulSoup
from datetime import datetime

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Threat keywords
THREAT_KEYWORDS = {"malware", "exploit", "hacker", "trojan", "ransomware", "carding", "ddos", "rootkit"}

# Ensure the data folder exists
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# Threat classification using NLP
def classify_threat(text):
    doc = nlp(text)
    if any(token.lemma_ in THREAT_KEYWORDS for token in doc):
        return "High-Risk"
    elif len(doc.ents) > 2:  # If multiple named entities exist, classify as Moderate-Risk
        return "Moderate-Risk"
    else:
        return "Low-Risk"

# Extract product details from the local file
def parse_marketplace(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    products = []

    for item in soup.select(".product-listing"):  # Select all product entries
        try:
            name = item.select_one(".product-title").text.strip()
            description = item.select_one(".product-description").text.strip()
            vendor = item.select_one(".vendor-name").text.strip()
            rating = item.select_one(".vendor-rating").text.strip()
            timestamp = item.select_one(".timestamp").text.strip()
            transaction_history = [tx.text.strip() for tx in item.select(".transaction-history .entry")]

            # Keyword-based detection (Replaced `word_tokenize()` with `.split()`)
            words = set(description.lower().split())  
            keyword_alert = words.intersection(THREAT_KEYWORDS)

            # ML-based classification
            threat_level = classify_threat(description)

            # Alert Trigger
            if keyword_alert:
                print(f"🚨 [Keyword Detection] {name} contains threat keywords: {keyword_alert}")

            if threat_level != "Low-Risk":
                print(f"⚠️ [ML Alert] {name} classified as {threat_level} risk!")

            products.append({
                "name": name,
                "description": description,
                "vendor": vendor,
                "rating": rating,
                "timestamp": timestamp,
                "transaction_history": transaction_history,
                "keyword_alerts": list(keyword_alert),
                "threat_level": threat_level
            })
        except AttributeError:
            continue  # Skip if any element is missing

    return products

# Scrape the local HTML file
def scrape_local_html():
    html_file_path = "test_market.html"  # File containing fake dark web listings

    if not os.path.exists(html_file_path):
        print(f"[-] Error: {html_file_path} not found!")
        return

    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    print("[+] Parsing local HTML file...")
    structured_data = parse_marketplace(html_content)

    # Save structured JSON data
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(DATA_FOLDER, f"fake_darkweb_scrape_{timestamp_str}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4, ensure_ascii=False)

    print(f"[+] Data saved in {file_path} ({len(structured_data)} entries found)")

# Run the scraper
if __name__ == "__main__":
    scrape_local_html()
