import argparse
import time
import urllib.parse
import base64
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- Argumente einlesen ---
parser = argparse.ArgumentParser(description="Scrape business listings from Gelbeseiten by industry and city.")
parser.add_argument("industry", help="Industry to search for, e.g. 'Tischler'")
parser.add_argument("city", help="City to search in, e.g. 'Frankfurt am Main'")
args = parser.parse_args()

# --- URL vorbereiten ---
base_url = "https://www.gelbeseiten.de/branchen"
industry_encoded = urllib.parse.quote(args.industry)
city_encoded = urllib.parse.quote(args.city)
url = f"{base_url}/{industry_encoded}/{city_encoded}"

# --- Selenium-Browser vorbereiten ---
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-extensions")
options.add_argument("--log-level=3")

service = Service()
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")
entries = soup.find_all("article", class_="mod mod-Treffer")

for i, entry in enumerate(entries, 1):
    # Name
    name_tag = entry.find("h2")
    name = name_tag.text.strip() if name_tag else "No Name"

    address_div = entry.find("div", class_="mod-AdresseKompakt__adress-text")
    address = " ".join(address_div.stripped_strings) if address_div else "No Address"

    phone_tag = entry.find("a", class_="mod-TelefonnummerKompakt__phoneNumber")
    phone = phone_tag.text.strip() if phone_tag else "No Phone Number"

    website = "No Website"
    website_span = entry.find("span", class_="mod-WebseiteKompakt__text")
    if website_span and website_span.has_attr("data-webseitelink"):
        try:
            encoded = website_span['data-webseitelink']
            website = base64.b64decode(encoded).decode('utf-8')
        except Exception:
            website = "Invalid Website (Decode Error)"

    print(f"{i}. {name}")
    print(f"   Address: {address}")
    print(f"   Phone:   {phone}")
    print(f"   Website: {website}\n")

driver.quit()
