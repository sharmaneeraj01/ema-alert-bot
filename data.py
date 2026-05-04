import yfinance as yf

def get_ema_signal(symbol):
    try:
        data = yf.download(symbol + ".NS", period="2mo", interval="1d", progress=False)

        if data.empty or len(data) < 21:
            return None

        data["EMA21"] = data["Close"].ewm(span=21, adjust=False).mean()

        latest = data.iloc[-1]

        close = latest["Close"]
        ema = latest["EMA21"]

        return {
            "symbol": symbol,
            "close": round(close, 2),
            "ema": round(ema, 2),
            "below": close < ema
        }

    except Exception as e:
        print(f"Error: {symbol} → {e}")
        return None
