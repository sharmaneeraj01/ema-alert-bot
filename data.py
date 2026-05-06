import yfinance as yf
import pandas as pd

def get_ema_signal(symbol):
    try:
        df = yf.download(symbol + ".NS", period="3mo", interval="1d", progress=False)

        if df.empty or len(df) < 55:
            return None

        df = df[['Close']].dropna()

        # EMA calculations
        df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()
        df["EMA55"] = df["Close"].ewm(span=55, adjust=False).mean()

        # Get last two rows
        today = df.iloc[-1]
        yesterday = df.iloc[-2]

        # Prices
        today_close = float(today["Close"].item())
        yest_close = float(yesterday["Close"].item())

        # EMA21
        today_ema21 = float(today["EMA21"].item())
        yest_ema21 = float(yesterday["EMA21"].item())

        # EMA55
        today_ema55 = float(today["EMA55"].item())
        yest_ema55 = float(yesterday["EMA55"].item())

        # Breakdown logic (event-based)
        breakdown_21 = (yest_close > yest_ema21) and (today_close < today_ema21)
        breakdown_55 = (yest_close > yest_ema55) and (today_close < today_ema55)

        return {
            "symbol": symbol,
            "close": round(today_close, 2),
            "ema21": round(today_ema21, 2),
            "ema55": round(today_ema55, 2),
            "breakdown_21": breakdown_21,
            "breakdown_55": breakdown_55
        }

    except Exception as e:
        print(f"Error: {symbol} → {e}")
        return None
