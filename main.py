from data import get_ema_signal
from telegram import send_to_telegram
from tabulate import tabulate

def load_watchlist():
    with open("watchlist.txt") as f:
        return [line.strip() for line in f if line.strip()]

def run():
    stocks = load_watchlist()

    rows = []   # ✅ MUST be here (inside run, before loop)

    for stock in stocks:
        result = get_ema_signal(stock)

        if not result:
            continue

        if result["breakdown"]:
            rows.append([
                stock,
                result["close"],
                result["ema"],
                "❌ Breakdown"
            ])

    # AFTER loop
    if rows:
        table = tabulate(
            rows,
            headers=["Stock", "Close", "EMA21", "Signal"],
            tablefmt="github"
        )

        message = (
            "🚨 *EMA 21 Breakdown Alert*\n\n"
            "```\n"
            f"{table}\n"
            "```"
        )
    else:
        message = "✅ No EMA breakdown signals today"

    print(message)
    send_to_telegram(message)

if __name__ == "__main__":
    run()
