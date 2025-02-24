import requests
from bs4 import BeautifulSoup
import os
import re

# Configuration
SAVE_DIR = r"W:\GIT\automation"
os.makedirs(SAVE_DIR, exist_ok=True)

# Unwanted words/patterns
UNWANTED_WORDS = {
    "Facebook", "X (Twitter)", "Email", "Copy Link", 
    "schoolLearn More", "On This Day in History", ","
}
DATE_PATTERN = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?\b", re.IGNORECASE)

def scrape_holidays(month, day, year):
    url = f"https://www.checkiday.com/{month}/{day}/{year}/"
    print(f"🔍 Fetching holidays for {year}-{month:02d}-{day:02d} from {url}")

    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        print(f"✅ Response status: {response.status_code}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        holidays = [event.text.strip() for event in soup.select(".holiday a")]

        print(f"📌 Found {len(holidays)} raw holidays.")

        cleaned_holidays = []
        for holiday in holidays:
            original_holiday = holiday
            holiday = DATE_PATTERN.sub("", holiday)  # Remove date mentions
            holiday = holiday.strip()
            
            if holiday and holiday not in UNWANTED_WORDS:
                cleaned_holidays.append(holiday)
            else:
                print(f"❌ Removed unwanted text: '{original_holiday}'")

        print(f"✅ Cleaned holidays: {cleaned_holidays}\n")
        return cleaned_holidays or ["No holidays found"]
    
    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")
        return None

def process_holidays(year):
    print(f"\n🚀 Processing holidays for the year {year}...\n")
    
    all_holidays = []
    all_months = {
        1: 31
    }

    for month, days in all_months.items():
        for day in range(1, days + 1):
            holidays = scrape_holidays(month, day, year)
            if holidays:
                all_holidays.append(f"{year}-{month:02d}-{day:02d}: " + ", ".join(holidays))

    print(f"\n✅ Finished processing holidays for {year}. Total entries: {len(all_holidays)}\n")
    return all_holidays

def save_holidays_to_txt(holidays, file_name):
    print(f"💾 Saving holidays to {file_name}...")
    with open(file_name, "w") as f:
        for holiday in holidays:
            f.write(holiday + "\n")
    print(f"✅ Saved successfully!\n")

def main():
    year = 2025  # Change this to the desired year
    holidays = process_holidays(year)

    if not holidays:
        print("❌ No holidays found. Exiting.")
        return

    # Save to a text file
    file_name = f"{SAVE_DIR}/holidays_{year}.txt"
    save_holidays_to_txt(holidays, file_name)

    # Download the file
    print(f"📂 Response saved to '{file_name}' and downloaded.")

if __name__ == "__main__":
    main()
