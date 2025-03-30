import os
import requests
from bs4 import BeautifulSoup
import json
import spacy
from datetime import datetime

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Configure Tor Proxy (If needed)
TOR_SOCKS_PROXY = "socks5h://127.0.0.1:9050"
DARKWEB_MARKET_URL = "http://examplemarket.onion"  # Replace with a real onion URL

# Keyword-based threat detection list
THREAT_KEYWORDS = {"malware", "exploit", "hacker", "trojan", "ransomware", "carding", "ddos", "rootkit"}

# Ensure the data folder exists
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# Sample ML model (replace with an actual trained model)
def classify_threat(text):
    doc = nlp(text)
    if any(token.lemma_ in THREAT_KEYWORDS for token in doc):
        return "High-Risk"
    elif len(doc.ents) > 2:  # If multiple named entities are found, it's suspicious
        return "Moderate-Risk"
    else:
        return "Low-Risk"

# Create a session using Tor
def get_tor_session():
    session = requests.Session()
    session.proxies = {"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY}
    return session

# Extract product details
def parse_marketplace(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    products = []

    for item in soup.select(".product-listing"):
        try:
            name = item.select_one(".product-title").text.strip()
            description = item.select_one(".product-description").text.strip()
            vendor = item.select_one(".vendor-name").text.strip()
            rating = item.select_one(".vendor-rating").text.strip()
            timestamp = item.select_one(".timestamp").text.strip()
            transaction_history = [tx.text.strip() for tx in item.select(".transaction-history .entry")]

            # Use Python's built-in `split()` instead of `word_tokenize()`
            words = set(description.lower().split())  
            keyword_alert = words.intersection(THREAT_KEYWORDS)

            # ML-based classification
            threat_level = classify_threat(description)

            # Alert Trigger
            if keyword_alert:
                print(f"🚨 [Keyword Detection] Threat Detected: {name} - {keyword_alert}")

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

# Scraper function
def scrape_darkweb_market():
    session = get_tor_session()

    try:
        response = session.get(DARKWEB_MARKET_URL, timeout=10)
        if response.status_code == 200:
            print("[+] Successfully accessed the marketplace")
            structured_data = parse_marketplace(response.text)

            # Save structured JSON data
            timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(DATA_FOLDER, f"darkweb_threats_{timestamp_str}.json")

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(structured_data, f, indent=4, ensure_ascii=False)

            print(f"[+] Data saved in {file_path} ({len(structured_data)} threats detected)")
        else:
            print(f"[-] Failed to access marketplace, status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"[-] Connection error: {e}")

# Run the scraper
if __name__ == "__main__":
    scrape_darkweb_market()
