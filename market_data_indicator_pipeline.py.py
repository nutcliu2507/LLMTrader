# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd
import numpy as np


# =========================
# 1. 基本設定
# =========================

TICKERS = {
    "BTC": "BTC-USD",
    "NVDA": "NVDA",
    "TSM": "TSM",
    "GOLD": "GC=F"
}

START_DATE = "2023-04-01"
END_DATE = "2025-01-01"


# =========================
# 2. 技術指標函數
# =========================

def calculate_rsi(close, window=14):
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_atr(df, window=14):
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = true_range.ewm(alpha=1 / window, adjust=False).mean()

    return atr


def calculate_adx(df, window=14):
    high = df["High"]
    low = df["Low"]

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = np.where(
        (up_move > down_move) & (up_move > 0),
        up_move,
        0
    )

    minus_dm = np.where(
        (down_move > up_move) & (down_move > 0),
        down_move,
        0
    )

    plus_dm = pd.Series(plus_dm, index=df.index)
    minus_dm = pd.Series(minus_dm, index=df.index)

    atr = calculate_atr(df, window)

    plus_di = 100 * plus_dm.ewm(alpha=1 / window, adjust=False).mean() / atr
    minus_di = 100 * minus_dm.ewm(alpha=1 / window, adjust=False).mean() / atr

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)

    adx = dx.ewm(alpha=1 / window, adjust=False).mean()

    return adx, plus_di, minus_di


def calculate_macd(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()

    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - macd_signal

    return macd, macd_signal, macd_hist


def calculate_bollinger_bands(close, window=20, num_std=2):
    middle = close.rolling(window=window).mean()
    std = close.rolling(window=window).std()

    upper = middle + num_std * std
    lower = middle - num_std * std

    return lower, middle, upper


def calculate_obv(df):
    close = df["Close"]
    volume = df["Volume"]

    direction = np.sign(close.diff()).fillna(0)
    obv = (direction * volume).cumsum()

    return obv


def calculate_stochastic(df, k_window=14, d_window=3):
    low_min = df["Low"].rolling(window=k_window).min()
    high_max = df["High"].rolling(window=k_window).max()

    stoch_k = 100 * (df["Close"] - low_min) / (high_max - low_min)

    stoch_k_smooth = stoch_k.rolling(window=d_window).mean()
    stoch_d = stoch_k_smooth.rolling(window=d_window).mean()

    return stoch_k_smooth, stoch_d


# =========================
# 3. 加入技術指標
# =========================

def add_technical_indicators(df):
    df = df.copy()

    df = df.dropna(subset=["Open", "High", "Low", "Close"])

    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()

    df["RSI_14"] = calculate_rsi(df["Close"], window=14)

    df["ATR_14"] = calculate_atr(df, window=14)

    df["ADX_14"], df["PLUS_DI_14"], df["MINUS_DI_14"] = calculate_adx(df, window=14)

    (
        df["BB_Lower_20_2"],
        df["BB_Middle_20"],
        df["BB_Upper_20_2"]
    ) = calculate_bollinger_bands(df["Close"], window=20, num_std=2)

    (
        df["MACD_12_26"],
        df["MACDsignal_9"],
        df["MACDhist"]
    ) = calculate_macd(df["Close"], fast=12, slow=26, signal=9)

    df["OBV"] = calculate_obv(df)

    (
        df["Stoch_%K_14_3"],
        df["Stoch_%D_3"]
    ) = calculate_stochastic(df, k_window=14, d_window=3)

    return df


# =========================
# 4. 數字格式化
# =========================

def fmt(value, digits=4):
    """
    把數值轉成比較乾淨的文字。
    如果是 NaN，顯示為 N/A。
    """
    if pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):.{digits}f}"
    except:
        return str(value)


# =========================
# 5. 每日資訊彙整欄位
# =========================

def create_daily_info(row):
    daily_info = f"""日期：{row["Date"].strftime("%Y/%m/%d")}
商品：{row["Asset"]}
代號：{row["Ticker"]}

開：{fmt(row["Open"])}
高：{fmt(row["High"])}
低：{fmt(row["Low"])}
收：{fmt(row["Close"])}
成交量：{fmt(row["Volume"], 0)}

各種技術指標：
ADX_14：{fmt(row["ADX_14"])}
ATR_14：{fmt(row["ATR_14"])}
BB_Lower_20_2：{fmt(row["BB_Lower_20_2"])}
BB_Middle_20：{fmt(row["BB_Middle_20"])}
BB_Upper_20_2：{fmt(row["BB_Upper_20_2"])}
MACD_12_26：{fmt(row["MACD_12_26"])}
MACDhist：{fmt(row["MACDhist"])}
MACDsignal_9：{fmt(row["MACDsignal_9"])}
MINUS_DI_14：{fmt(row["MINUS_DI_14"])}
OBV：{fmt(row["OBV"], 0)}
PLUS_DI_14：{fmt(row["PLUS_DI_14"])}
RSI_14：{fmt(row["RSI_14"])}
SMA_200：{fmt(row["SMA_200"])}
SMA_50：{fmt(row["SMA_50"])}
Stoch_%D_3：{fmt(row["Stoch_%D_3"])}
Stoch_%K_14_3：{fmt(row["Stoch_%K_14_3"])}
"""
    return daily_info


# =========================
# 6. 下載、計算、分別存檔
# =========================

def download_and_process_data():
    all_data = []

    for asset_name, ticker in TICKERS.items():
        print(f"Downloading {asset_name} ({ticker})...")

        df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            print(f"Warning: No data found for {asset_name}")
            continue

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]

        df = add_technical_indicators(df)

        df.insert(0, "Asset", asset_name)
        df.insert(1, "Ticker", ticker)

        df.reset_index(inplace=True)

        # 確保 Date 是 datetime 格式
        df["Date"] = pd.to_datetime(df["Date"])

        # 新增每日資訊彙整欄位
        df["Daily_Info"] = df.apply(create_daily_info, axis=1)

        # 調整欄位順序，把 Daily_Info 放前面一點
        column_order = [
            "Date",
            "Asset",
            "Ticker",
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
            "SMA_50",
            "SMA_200",
            "RSI_14",
            "ATR_14",
            "ADX_14",
            "PLUS_DI_14",
            "MINUS_DI_14",
            "BB_Lower_20_2",
            "BB_Middle_20",
            "BB_Upper_20_2",
            "MACD_12_26",
            "MACDsignal_9",
            "MACDhist",
            "OBV",
            "Stoch_%D_3",
            "Stoch_%K_14_3",
            "Daily_Info"
        ]

        df = df[column_order]

        # 每個商品分別存一個檔案
        output_file = f"{asset_name}_indicators.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")

        print(f"Saved: {output_file}")

        all_data.append(df)

    if not all_data:
        raise ValueError("No data downloaded. Please check tickers or internet connection.")

    # 額外也存一份全部商品合併檔
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(
        "ALL_assets_indicators.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Saved: ALL_assets_indicators.csv")

    return final_df


# =========================
# 7. 主程式
# =========================

if __name__ == "__main__":
    final_df = download_and_process_data()

    print("\nDone!")
    print("已完成以下檔案：")
    print("- BTC_indicators.csv")
    print("- NVDA_indicators.csv")
    print("- TSM_indicators.csv")
    print("- GOLD_indicators.csv")
    print("- ALL_assets_indicators.csv")

    print("\nPreview:")
    print(final_df.head())


    