import requests
import datetime
from bs4 import BeautifulSoup
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import gspread
import time

OPENAI_API_KEY = "your_openai_api_key"
GENAI_API_KEY = "your_gemini_api_key"
SERVICE_ACCOUNT_FILE = "path/to/your-service-account.json"

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive"
]

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
docs_service = build("docs", "v1", credentials=creds)
sheets_client = gspread.authorize(creds)
calendar_service = build("calendar", "v3", credentials=creds)
drive_service = build("drive", "v3", credentials=creds)

def fetch_events():
    url = "https://www.timeanddate.com/holidays/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        events = []
        year = datetime.datetime.now().year
        
        for row in soup.select("#holidays-table tr:not(.thd)"):
            cols = row.find_all("td")
            if len(cols) >= 4:
                try:
                    date_str = f"{year} {cols[0].text.strip()}"
                    event_date = datetime.datetime.strptime(date_str, "%Y %b %d").date()
                    if event_date >= datetime.date.today():
                        events.append({"date": event_date.strftime("%Y-%m-%d"), "name": cols[3].text.strip()})
                except:
                    continue
        return events
    except:
        return []

def generate_post(name, date):
    try:
        prompt = f"Create a LinkedIn post for '{name}' on {date} that connects to travel experiences, mentions Safarnow naturally, includes 3 hashtags, has an engaging hook, and uses a friendly, professional tone."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            api_key=OPENAI_API_KEY
        )
        return response.choices[0].message.content
    except:
        return None

def generate_image():
    try:
        from google import genai
        client = genai.Client(api_key=GENAI_API_KEY)
        prompt = "A square diary character with a mischievous grin, wearing a tiny backpack and holding a tiny globe. His limbs are directly connected to his diary body, and he has a playful sparkle in his eyes."
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(
                aspect_ratio="16:9",
                safety_filter="strict",
                output_format="jpeg"
            )
        )
        return response.images[0].image_uri
    except:
        return None

def save_to_doc(name, content, image_url):
    try:
        doc = docs_service.documents().create().execute()
        doc_id = doc["documentId"]
        img_data = requests.get(image_url).content
        media = MediaIoBaseUpload(BytesIO(img_data), mimetype="image/jpeg")
        file_metadata = {"name": f"{name.replace(' ', '_')}_image.jpg"}
        image_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        requests = [
            {"insertText": {"location": {"index": 1}, "text": f"{name}\n\n{content}\n\n"}},
            {"insertInlineImage": {"location": {"index": 3}, "uri": f"https://drive.google.com/uc?id={image_file['id']}", "objectSize": {"width": {"magnitude": 500, "unit": "PT"}}}}
        ]
        docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
        return f"https://docs.google.com/document/d/{doc_id}"
    except:
        return None

def add_to_sheet(name, date, doc_link):
    try:
        sheet = sheets_client.open("Safarnow Events").sheet1
        sheet.append_row([datetime.datetime.now().isoformat(), name, date, doc_link])
        return True
    except:
        return False

def add_to_calendar(name, date, doc_link):
    try:
        reminder_date = (datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        event = {
            "summary": f"📅 Post: {name}",
            "start": {"date": reminder_date},
            "end": {"date": reminder_date},
            "description": f"Generated post: {doc_link}",
            "reminders": {"useDefault": False, "overrides": [{"method": "email", "minutes": 1440}, {"method": "popup", "minutes": 60}]}
        }
        calendar_service.events().insert(calendarId="primary", body=event).execute()
        return True
    except:
        return False

def main():
    events = fetch_events()
    for event in events:
        name, date = event["name"], event["date"]
        post_content = generate_post(name, date)
        if not post_content:
            continue
        image_url = generate_image()
        if not image_url:
            continue
        doc_link = save_to_doc(name, post_content, image_url)
        if not doc_link:
            continue
        add_to_sheet(name, date, doc_link)
        add_to_calendar(name, date, doc_link)
        time.sleep(5)

if __name__ == "__main__":
    main()
