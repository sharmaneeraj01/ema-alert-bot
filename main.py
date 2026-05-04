from data import get_ema_signal
from telegram import send_to_telegram

def load_watchlist():
    with open("watchlist.txt") as f:
        return [line.strip() for line in f if line.strip()]

def run():
    stocks = load_watchlist()
    alerts = []

    for stock in stocks:
        result = get_ema_signal(stock)

        if not result:
            continue

        if result["below"]:
            alerts.append(
                f"{stock} ❌ Close:{result['close']} < EMA21:{result['ema']}"
            )

    if alerts:
        message = "🚨 *EMA 21 Breakdown Alert*\n\n" + "\n".join(alerts)
    else:
        message = "✅ No stocks below EMA21 today"

    print(message)
    send_to_telegram(message)

if __name__ == "__main__":
    run()
