import csv
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import json
import os

def save_text_to_json(url):
    try:
        response = requests.get(url, timeout=(5, 30))
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        text = soup.get_text(strip=True)

        domain = url.split("//")[-1].split("/")[0]

        data = {
            "domain": domain,
            "text": text
        }
        os.makedirs("data", exist_ok=True)
        filename = f"data/{domain}.json"

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        print(f"Data saved for {domain}")
    except Exception as e:
        print(f"Failed to process {url}: {str(e)}")

def main(csv_filename):
    urls = []
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.append("https://" + row[1])

    with ThreadPoolExecutor(max_workers=7) as executor:
        executor.map(save_text_to_json, urls)

if __name__ == "__main__":
    main("websites.csv")
