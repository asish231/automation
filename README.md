# AI-Powered Web Scraper

## Overview
This is an advanced web scraper that dynamically finds relevant websites, extracts content, and utilizes the Gemini AI API to format and enhance the extracted data. The scraper ensures efficiency, reliability, and user interactivity.

## Features
- Dynamic Website Selection – Automatically searches for relevant websites using Google Search.
- Comprehensive Scraping – Extracts text from `<h1>`, `<h2>`, `<h3>`, `<p>`, and `<li>` elements.
- AI-Powered Formatting – Uses the Gemini API to structure and enhance the extracted data.
- Custom Output Format – Asks the user about their preferred format before sending data to AI.
- Error Handling – Prevents crashes if a website blocks scraping.
- File Saving Option – Allows users to save the formatted output as a `.txt` file.

## Requirements
Ensure you have the following installed:
- Python 3.x
- `requests` (For HTTP requests)
- `BeautifulSoup` (For web scraping)
- `google-search-results` (For dynamic website discovery)
- `selenium` (For automated browsing)
- `google` (For Gemini API interaction)

Install dependencies using:
```bash
pip install requests beautifulsoup4 google-search-results selenium google-generativeai
```

## Usage
### Run in Google Colab (Online)
1. Open [Google Colab](https://colab.research.google.com/).
2. Paste the script into a new notebook.
3. Visit [Google AI Studio](https://aistudio.google.com/) and click **Create API Key** after selecting a project.
4. Copy and paste your API key into the program.
5. Run the script by clicking the **Run** button.

### Run in Local Python Environment
1. Install the required libraries.
2. Add your Gemini API key in the script:
   ```python
   API_KEY = "your_gemini_api_key"
   ```
3. Open a terminal or command prompt.
4. Navigate to the folder where your script is saved.
5. Run the script using:
   ```bash
   python <filename_of_the_scraper>.py
   ```
   *(Replace `<filename_of_the_scraper>` with the actual file name of your script.)*

## Libraries Used
```python
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
from google import genai
```

## Limitations
- Some websites may block scraping.
- API usage may be limited based on the plan.

## Future Improvements
- Support for other AI models (e.g., GPT, Claude)
- Exporting data in different formats (JSON, CSV, PDF)
- Enhanced natural language processing for better summarization

**Made by Asish Kumar Sharma**  
Visit [SafarNow](https://safarnow.in) for more projects!

