Market Data Indicator Pipeline
Project Description
This project provides a Python-based data collection and technical indicator calculation pipeline. The program downloads historical daily market data from Yahoo Finance and calculates multiple technical indicators for selected financial assets.
The selected assets include:
BTC: Bitcoin, using the ticker `BTC-USD`
NVDA: NVIDIA Corporation, using the ticker `NVDA`
TSM: Taiwan Semiconductor Manufacturing Company, using the ticker `TSM`
GOLD: Gold Futures, using the ticker `GC=F`
The data period ranges from `2023-04-01` to `2025-01-01`.
Main Features
The program performs the following tasks:
Downloads historical OHLCV data from Yahoo Finance.
Calculates technical indicators.
Generates a daily textual summary column.
Exports each asset as an individual CSV file.
Exports all assets into a combined CSV file.
Technical Indicators
The following technical indicators are calculated:
SMA_50
SMA_200
RSI_14
ATR_14
ADX_14
PLUS_DI_14
MINUS_DI_14
BB_Lower_20_2
BB_Middle_20
BB_Upper_20_2
MACD_12_26
MACDsignal_9
MACDhist
OBV
Stoch_%K_14_3
Stoch_%D_3
Programming Environment
The program was developed and executed in the following environment:
Item	Specification
Operating System	Windows 11 Pro 64-bit
System Version	25H2
OS Build	26200.8037
Processor	11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
Memory	16.0 GB RAM
Programming Language	Python
Main Packages	yfinance, pandas, numpy
Data Source	Yahoo Finance
Data Frequency	Daily
Data Period	2023-04-01 to 2025-01-01
Installation
Step 1: Download the Project
Download the project files and place them in a project folder.
Example folder name:
```bash
market_data_indicator_project
```
Step 2: Create a Virtual Environment
```bash
python -m venv venv
```
Step 3: Activate the Virtual Environment
For Windows:
```bash
venv\Scripts\activate
```
For macOS or Linux:
```bash
source venv/bin/activate
```
Step 4: Install Required Packages
```bash
pip install -r requirements.txt
```
Usage
Run the Python script with the following command:
```bash
python market_data_indicator_pipeline.py
```
Output Files
After execution, the program will generate the following CSV files:
```text
BTC_indicators.csv
NVDA_indicators.csv
TSM_indicators.csv
GOLD_indicators.csv
ALL_assets_indicators.csv
```
Each individual CSV file contains the original OHLCV data, calculated technical indicators, and a `Daily_Info` column that summarizes the daily market information and indicators in text format.
Output Columns
The output dataset includes the following columns:
```text
Date
Asset
Ticker
Open
High
Low
Close
Adj Close
Volume
SMA_50
SMA_200
RSI_14
ATR_14
ADX_14
PLUS_DI_14
MINUS_DI_14
BB_Lower_20_2
BB_Middle_20
BB_Upper_20_2
MACD_12_26
MACDsignal_9
MACDhist
OBV
Stoch_%D_3
Stoch_%K_14_3
Daily_Info
```
Notes
Some technical indicators require a minimum number of historical data points before valid values can be calculated. For example, `SMA_200` requires at least 200 trading days. Therefore, missing values may appear in the early rows of the dataset. This is expected and does not indicate an error in the program.
Recommended Script Name
The recommended name for the main Python script is:
```text
market_data_indicator_pipeline.py
```
This name reflects the main purpose of the program, which is to collect market data, calculate technical indicators, and export the processed datasets.
