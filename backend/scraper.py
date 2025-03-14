import requests
from bs4 import BeautifulSoup
import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

LEADS_FILE = "backend/leads.json"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/537.36"
]

# ✅ Load existing leads
def load_leads():
    try:
        with open(LEADS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ✅ Save new leads
def save_leads(leads):
    with open(LEADS_FILE, "w") as file:
        json.dump(leads, file, indent=4)

# ✅ Scraper function for Bing
def scrape_bing(search_query, location):
    search_url = f"https://www.bing.com/search?q={search_query}+in+{location}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    business_results = []
    
    # ✅ Extract business names
    for result in soup.select("li.b_algo h2 a"):
        business_name = result.get_text(strip=True)
        if business_name:
            business_results.append({"name": business_name, "contacted": False})

    return business_results

# ✅ Scraper function for DuckDuckGo (Backup if Bing fails)
def scrape_duckduckgo(search_query, location):
    search_url = f"https://duckduckgo.com/html/?q={search_query}+in+{location}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    business_results = []
    
    for result in soup.select("a.result__a"):
        business_name = result.get_text(strip=True)
        business_results.append({"name": business_name, "contacted": False})

    return business_results

# ✅ Main scraper function that chooses Bing or DuckDuckGo
def scrape_businesses(search_query, location):
    leads = scrape_bing(search_query, location)

    if not leads:  # 🔥 If Bing fails, try DuckDuckGo
        print("⚠️ No results from Bing. Trying DuckDuckGo...")
        leads = scrape_duckduckgo(search_query, location)

    return leads

# ✅ API Endpoint to Scrape Leads
@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    search_query = data.get("search_query")
    location = data.get("location")

    if not search_query or not location:
        return jsonify({"error": "Missing search query or location"}), 400

    leads = scrape_businesses(search_query, location)
    save_leads(leads)

    return jsonify({"message": "✅ Leads scraped successfully!", "leads": leads})

# ✅ API Endpoint to Get All Leads (For Dashboard)
@app.route("/get-leads", methods=["GET"])
def get_leads():
    return jsonify(load_leads())

if __name__ == "__main__":
    app.run(debug=True, port=5002)
