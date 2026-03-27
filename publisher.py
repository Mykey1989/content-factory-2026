import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID_ARTICLES")

def publish_to_notion():
    if not DATABASE_ID or "ここに" in DATABASE_ID:
        print("Error: NOTION_DATABASE_ID_ARTICLES が正しく設定されていません。")
        return

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # 記事データの準備（簡易版：タイトルとステータスのみ）
    # 本来は content_generator からタイトルを動的に取得するが、今回はテーマを固定
    data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Title": {
                "title": [
                    { "text": { "content": "生成AIと歩む「人生100年時代」のキャリア戦略ロードマップ" } }
                ]
            },
            "Status": {
                "select": { "name": "Draft" }
            },
            "Category": {
                "select": { "name": "Career" }
            },
            "Slug": {
                "rich_text": [{ "text": { "content": "life-100-ai-career-roadmap" } }]
            }
        }
    }
    
    print("Project A: Publishing to Notion CMS...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Success: Page created in ContentFactory_Articles database.")
        print(f"URL: {response.json().get('url')}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    publish_to_notion()
