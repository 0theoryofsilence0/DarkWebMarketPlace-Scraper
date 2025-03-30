# Dark Web Scraper

## Dependencies

The following dependencies are required:

- `requests[socks]`
- `beautifulsoup4`
- `spacy`
- `scikit-learn`

## Installation

### 1. Create a Virtual Environment
Bash:
```bash
python3 -m venv venv
```
Windows:
```windows
python -m venv venv
```

### 2. Install Dependencies
Bash:
```bash
pip install requests[socks] beautifulsoup4 spacy scikit-learn
python3 -m spacy download en_core_web_sm
```
Windows:
```windows
pip install requests[socks] beautifulsoup4 spacy scikit-learn
python3 -m spacy download en_core_web_sm
```

### 3. Activate the Virtual Environment
Bash:
```bash
source venv/bin/activate
```
Windows:
```windows
venv\Scripts\activate
```

## 4. Create a folder Named Data

## Running the Scraper

- **For Local Execution:**
  ```bash
  python3 darkweb_scraper_local.py
  ```

- **For Live Execution:**
  ```bash
  python3 darkweb_scraper_live.py
  ```

