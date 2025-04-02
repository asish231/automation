import requests
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
from google import genai

# Configure Gemini AI (Replace with your API Key)
client = genai.Client(api_key="Place_your_gemini_api_key")
''' to get the gemini api key visit ai studio from google and there on the very first option 
make use of the create api and then select or create a dummy project and its name and then
copy the api key''''

def find_websites(query, num_results=5):
    """Search Google for websites related to the user's topic."""
    return list(search(query, num=num_results, stop=num_results, pause=2))

def scrape_website(url):
    """Scrape data from a given website dynamically."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        text_data = []
        for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
            text_data.append(p.get_text(strip=True))
        
        return '\n'.join(text_data)
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

def process_with_ai(text_data, format_request):
    """Send scraped data to Gemini AI for formatting."""
    prompt = f"Format the following data in {format_request} format:\n{text_data}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text if response else "Error in AI processing."

def save_to_file(data, filename="scraped_data.txt"):
    """Save data to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)
    print(f"Data saved as {filename}")

def main():
    user_query = input("Enter what you want to scrape: ")
    print("Searching for websites...")
    websites = find_websites(user_query)
    
    if not websites:
        print("No relevant websites found.")
        return
    
    print("Websites found:")
    for idx, site in enumerate(websites, start=1):
        print(f"{idx}. {site}")
    
    all_data = ""
    for site in websites:
        print(f"Scraping {site}...")
        data = scrape_website(site)
        all_data += f"\n\nData from {site}:\n" + data
    
    print("Data extraction complete.")
    format_request = input("How do you want the data to be formatted? (e.g., summary, bullet points, table): ")
    formatted_data = process_with_ai(all_data, format_request)
    print("\nFormatted Data:")
    print(formatted_data)
    
    save_option = input("Do you want to save the data as a text file? (yes/no): ").strip().lower()
    if save_option == 'yes':
        save_to_file(formatted_data)

if __name__ == "__main__":
    main()
