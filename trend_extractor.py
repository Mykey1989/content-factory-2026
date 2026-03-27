import os
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configuration
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_trend_data():
    # トレンドソース（簡易版：Google News RSSなど）から取得
    # Project A要件に合わせて将来的にReddit/X/Amazon BSRへ拡張可能
    url = "https://news.google.com/rss/search?q=AI+business+trends&hl=ja&gl=JP&ceid=JP:ja"
    response = requests.get(url)
    return response.text[:5000]  # 長さ制限

def extract_high_roi_topics(raw_data):
    prompt = f"""
    Role: Senior Content Strategist
    Task: 以下のトレンドデータから、2026年現在の市場環境において「ROI 30%以上」が見込めるコンテンツ制作（KDP、Note、アフィリエイト）のネタを3つ抽出せよ。
    Data: {raw_data}
    
    Constraints:
    - 収益性（ROI）の根拠を数値で示すこと。
    - 競合が少なく、生成AIで高品質な初稿が書けるもの。
    - 出力はMarkdown形式。
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    print("Project A: Trend Extracting...")
    try:
        raw_trends = get_trend_data()
        high_roi_content = extract_high_roi_topics(raw_trends)
        
        # ログ保存
        with open("high_roi_trends.md", "w") as f:
            f.write(high_roi_content)
        
        print("Success: high_roi_trends.md generated.")
        print("-" * 30)
        print(high_roi_content)
    except Exception as e:
        print(f"Error: {e}")
