import yfinance as yf
import pandas as pd
import requests
import os
import time
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("COINMARKETCAP_API_KEY")

# 📂 Chemin des fichiers de données
DATA_PATH = "data/"

# 📦 Charger toutes les listes d'actifs
def load_assets():
    assets = {
        "usa_stocks": "usa_stocks.csv",
        "europe_stocks": "europe_stocks.csv",
        "asia_stocks": "asia_stocks.csv",
        "etfs": "etf_list.csv",
        "cryptos": "crypto_list.csv",
        "scpis": "scpi_list.csv"
    }
    
    loaded_assets = {}
    for key, file in assets.items():
        filepath = os.path.join(DATA_PATH, file)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            if "Symbol" in df.columns:
                loaded_assets[key] = df["Symbol"].tolist()
    
    return loaded_assets

# 📡 Télécharger les données depuis Yahoo Finance (actions, ETF, SCPI)
def fetch_yfinance_data(symbols):
    data = {}
    for i, symbol in enumerate(symbols):
        try:
            print(f"📡 {i+1}/{len(symbols)} : Récupération de {symbol}...")
            df = yf.download(symbol, period="max")
            if not df.empty:
                data[symbol] = df
            time.sleep(1)  # ⏳ Pause pour éviter un blocage de Yahoo
        except Exception as e:
            print(f"⚠️ Erreur avec {symbol} : {e}")
    return data

# 📡 Télécharger les prix des cryptos depuis CoinMarketCap
def fetch_crypto_data(symbols):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}
    params = {"start": 1, "limit": 5000, "convert": "USD"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        crypto_prices = {}
        for crypto in data["data"]:
            if crypto["symbol"] in symbols:
                crypto_prices[crypto["symbol"]] = crypto["quote"]["USD"]["price"]
        
        return crypto_prices
    except Exception as e:
        print(f"⚠️ Erreur API CoinMarketCap : {e}")
        return {}

# 🏦 Sauvegarde dans SQLite avec SQLAlchemy
def save_to_db(data_dict, table_prefix="yfinance_"):
    engine = create_engine("sqlite:///data/invest_data.db")

    for symbol, df in data_dict.items():
        table_name = table_prefix + symbol.replace("-", "_")  # Nettoyer le nom de table
        df.to_sql(table_name, con=engine, if_exists="replace", index=True)

# 🚀 Exécuter le pipeline complet
def main():
    print("📂 Chargement des actifs...")
    assets = load_assets()
    
    all_stocks = assets.get("usa_stocks", []) + assets.get("europe_stocks", []) + assets.get("asia_stocks", [])
    etfs = assets.get("etfs", [])
    cryptos = assets.get("cryptos", [])
    scpis = assets.get("scpis", [])
    
    print(f"📈 Nombre total d'actions & ETF : {len(all_stocks) + len(etfs)}")
    print(f"🪙 Nombre total de cryptos : {len(cryptos)}")
    print(f"🏠 Nombre total de SCPI : {len(scpis)}")

    # 🔹 Récupération des données
    print("📡 Récupération des actions & ETF...")
    stock_data = fetch_yfinance_data(all_stocks + etfs)
    
    print("📡 Récupération des cryptos...")
    crypto_prices = fetch_crypto_data(cryptos)
    
    print("📡 Récupération des SCPI...")
    scpi_data = fetch_yfinance_data(scpis)
    
    # 💾 Sauvegarde en base de données
    print("💾 Sauvegarde en base SQLite...")
    save_to_db(stock_data, "yfinance_")
    save_to_db(scpi_data, "yfinance_scpi_")
    
    # Sauvegarde des cryptos sous forme de DataFrame
    crypto_df = pd.DataFrame(list(crypto_prices.items()), columns=["Symbol", "Price"])
    engine = create_engine("sqlite:///data/invest_data.db")
    crypto_df.to_sql("crypto_prices", con=engine, if_exists="replace", index=False)

    print("✅ Toutes les données ont été enregistrées en base SQLite !")

if __name__ == "__main__":
    main()
