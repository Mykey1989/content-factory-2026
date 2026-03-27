import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_draft():
    # 前工程で抽出したトレンド案を読み込む
    with open("high_roi_trends.md", "r") as f:
        trends = f.read()

    prompt = f"""
    Role: Professional Content Creator
    Task: 以下の高ROIトレンド案の中から最もポテンシャルの高いものを1つ選び、Kindle書籍(KDP)向けの「詳細な章立て構成」と「導入部(序文)」を執筆せよ。
    Data: {trends}
    
    Constraint:
    - 読者のベネフィットを明確にすること。
    - 専門用語を噛み砕き、実践的なアクションプランを含めること。
    - Markdown形式で出力すること。
    """
    
    print("Project A: Generating Content Draft...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    try:
        draft = generate_draft()
        with open("kdp_draft_outline.md", "w") as f:
            f.write(draft)
        print("Success: kdp_draft_outline.md generated.")
        print("-" * 30)
        print(draft[:500] + "...") # 冒頭のみ表示
    except Exception as e:
        print(f"Error: {e}")
