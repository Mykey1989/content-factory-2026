import os
import datetime
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configuration
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
context_file = "project_context.md"

def fetch_notion_updates():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Notion API Error {response.status_code}: {response.text}")
        
    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"JSON Parse Error: {e} - Response: {response.text}")
        
    results = data.get("results", [])
    if not results:
        return ""

    summary_data = []
    
    for page in results:
        props = page.get("properties", {})
        
        # Title extraction
        title = "Unnamed Task"
        for key, val in props.items():
            if val.get("type") == "title":
                title_arr = val.get("title", [])
                if title_arr:
                    title = title_arr[0].get("plain_text", "Unnamed Task")
                break
        
        # Status extraction
        status = "Unknown Status"
        for key, val in props.items():
            if val.get("type") == "status":
                status = val.get("status", {}).get("name", "Unknown Status")
                break
            elif val.get("type") == "select":
                select_val = val.get("select")
                if select_val:
                    status = select_val.get("name", "Unknown Status")
                break
                
        summary_data.append(f"- {title} (Status: {status})")
    
    return "\n".join(summary_data)

def generate_summary(raw_data):
    prompt = f"""
    Role: Design Solution PM
    Task: 要約と差分抽出
    Data: {raw_data}
    Constraint: 簡潔に事実のみ。ROI評価を含める。
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def update_context(summary):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n### {timestamp} Notion Sync\n{summary}\n"
    with open(context_file, "a") as f:
        f.write(entry)

if __name__ == "__main__":
    print("Starting Mission 3 Sync...")
    try:
        data = fetch_notion_updates()
        if not data:
            print("No updates found in Notion.")
        else:
            summary = generate_summary(data)
            update_context(summary)
            print("Sync Complete: project_context.md updated.")
    except Exception as e:
        print(f"Error during sync: {e}")
