import ccxt
import time

def run_sentinel():
    print("--- Sentinel: FX/CFD Monitoring Start ---")
    exchange = ccxt.binance() # テスト用にBinanceを使用
    while True:
        try:
            ticker = exchange.fetch_ticker('BTC/USDT')
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] BTC: ${ticker['last']:,.2f}")
            time.sleep(10) # 10秒毎に更新
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    run_sentinel()
