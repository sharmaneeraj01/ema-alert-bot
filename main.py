from data import get_ema_signal
from telegram import send_to_telegram
from tabulate import tabulate


def load_watchlist():
    with open("watchlist.txt") as f:
        return [line.strip() for line in f if line.strip()]


def run():
    stocks = load_watchlist()
    rows = []

    for stock in stocks:
        result = get_ema_signal(stock)

        if not result:
            continue

        # Check if ANY breakdown happened
        if result["breakdown_21"] or result["breakdown_55"]:

            signals = []

            if result["breakdown_21"]:
                signals.append("EMA21")

            if result["breakdown_55"]:
                signals.append("EMA55")

            rows.append([
                stock,
                result["close"],
                result["ema21"],
                result["ema55"],
                ", ".join(signals)
            ])

    # Sort by strength (optional)
    rows.sort(key=lambda x: (x[2] - x[1]), reverse=True)

    # Build message
    if rows:
        table = tabulate(
            rows,
            headers=["Stock", "Close", "EMA21", "EMA55", "Breakdown"],
            tablefmt="github"
        )

        message = (
            "🚨 *EMA Breakdown Alert (21 & 55)*\n\n"
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
