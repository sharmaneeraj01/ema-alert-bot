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
        latest = df.iloc[-1]

        close = float(latest['Close'])
        ema = float(latest['EMA21'])

        return {
            "symbol": symbol,
            "close": round(close, 2),
            "ema": round(ema, 2),
            "below": close < ema
        }

    except Exception as e:
        print(f"Error: {symbol} → {e}")
        return None
