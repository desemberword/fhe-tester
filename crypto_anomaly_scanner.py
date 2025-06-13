import requests
import time
import statistics

API_URL = "https://api.coingecko.com/api/v3/simple/price"
COINS = ["bitcoin", "ethereum", "dogecoin", "solana", "cardano"]
VS_CURRENCY = "usd"
HISTORY = {coin: [] for coin in COINS}
THRESHOLD = 5  # % отклонения для сигнала

def fetch_prices():
    response = requests.get(API_URL, params={"ids": ",".join(COINS), "vs_currencies": VS_CURRENCY})
    return response.json()

def detect_anomalies(prices):
    for coin, data in prices.items():
        price = data[VS_CURRENCY]
        HISTORY[coin].append(price)
        
        if len(HISTORY[coin]) > 20:  # Храним последние 20 значений
            HISTORY[coin].pop(0)
        
        if len(HISTORY[coin]) > 5:
            avg = statistics.mean(HISTORY[coin])
            deviation = ((price - avg) / avg) * 100
            
            if abs(deviation) > THRESHOLD:
                print(f"🚨 АНОМАЛИЯ: {coin.upper()} сейчас {price}$ ({deviation:.2f}% от среднего {avg:.2f}$)")

def main():
    print("🚀 Crypto Anomaly Scanner запущен!")
    while True:
        try:
            prices = fetch_prices()
            detect_anomalies(prices)
        except Exception as e:
            print("Ошибка:", e)
        time.sleep(30)  # проверка каждые 30 секунд

if __name__ == "__main__":
    main()
