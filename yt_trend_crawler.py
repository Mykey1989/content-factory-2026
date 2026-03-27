import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "32c0b0c0d55b80d49825e05a9778b667" # FIRE_Strategy_Dashboard

def crawl_youtube():
    # 多言語検索クエリ（1日100回実行で quota 限界付近を攻める設定）
    queries = [
        "AI business trend 2026", "生成AI 最新 ニュース 2026", 
        "AI agent automation enterprise", "AI 自动化 趋势 2026",
        "tendances IA 2026", "AI Trendvorgaben 2026"
    ]
    
    for q in queries:
        yt_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={q}&type=video&order=date&maxResults=3&key={API_KEY}"
        try:
            res = requests.get(yt_url).json()
            for item in res.get("items", []):
                title = item["snippet"]["title"]
                url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                
                # Notion 投稿
                requests.post("https://api.notion.com/v1/pages", headers={
                    "Authorization": f"Bearer {NOTION_TOKEN}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json"
                }, json={
                    "parent": {"database_id": DATABASE_ID},
                    "properties": {
                        "Name": {"title": [{"text": {"content": f"[YT] {title}"}}]},
                        "Source": {"select": {"name": "YouTube"}},
                        "URL": {"url": url},
                        "ROI_Score": {"number": 95}
                    }
                })
        except Exception as e:
            print(f"Error for query {q}: {e}")

if __name__ == "__main__":
    print(f"[{datetime.datetime.now()}] Multilingual YouTube Crawl Start...")
    crawl_youtube()
    print("Done.")
