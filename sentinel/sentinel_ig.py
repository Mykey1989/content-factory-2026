import os
import time
from trading_ig import IGService
from dotenv import load_dotenv

load_dotenv()

def connect_ig():
    print("--- Mission 1: Sentinel IG Connectivity Test ---")
    ig_service = IGService(
        os.getenv("IG_USERNAME"),
        os.getenv("IG_PASSWORD"),
        os.getenv("IG_API_KEY"),
        "LIVE" # デモ口座の場合は "DEMO"
    )
    try:
        ig_service.create_session()
        print("✅ IG Markets Session: CONNECTED")
        
        # 口座情報の取得（リスク管理用）
        accounts = ig_service.fetch_accounts()
        print(f"Target Account: {os.getenv('IG_ACC_ID')}")
        print(accounts.loc[accounts['accountId'] == os.getenv('IG_ACC_ID')])
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    connect_ig()
