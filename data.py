import yfinance as yf
import pandas as pd

def get_ema_signal(symbol):
    try:
        df = yf.download(symbol + ".NS", period="2mo", interval="1d", progress=False)

        if df.empty or len(df) < 21:
            return None

        # Ensure clean dataframe
        df = df[['Close']].dropna()

        # Calculate EMA
        df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()

        # Get last row safely
        # Get last two rows
        today = df.iloc[-1]
        yesterday = df.iloc[-2]

        # Extract values safely
        today_close = float(today['Close'].item())
        today_ema = float(today['EMA21'].item())

        yest_close = float(yesterday['Close'].item())
        yest_ema = float(yesterday['EMA21'].item())

        # EVENT: crossed below EMA
        breakdown = (yest_close > yest_ema) and (today_close < today_ema)

        return {
            "symbol": symbol,
            "close": round(today_close, 2),
            "ema": round(today_ema, 2),
            "breakdown": breakdown
        }

    except Exception as e:
        print(f"Error: {symbol} → {e}")
        return None
