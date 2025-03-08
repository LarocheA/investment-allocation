import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import time

# 📥 Charger toutes les listes de symboles
usa_stocks = pd.read_csv("data/usa_stocks.csv")["Symbol"].tolist()
europe_stocks = pd.read_csv("data/europe_stocks.csv")["Symbol"].tolist()
asia_stocks = pd.read_csv("data/asia_stocks.csv")["Symbol"].tolist()
etfs = pd.read_csv("data/etf_list.csv")["Symbol"].tolist()
cryptos = pd.read_csv("data/crypto_list.csv")["Symbol"].tolist()

# 🎯 Fusionner toutes les catégories
assets = list(set(usa_stocks + europe_stocks + asia_stocks + etfs + [c + "-USD" for c in cryptos]))

print(f"🔍 Nombre total d'actifs à récupérer : {len(assets)}")

# 📊 Connexion à la base SQLite
engine = create_engine("sqlite:///data/invest_data.db")

for i, asset in enumerate(assets):
    try:
        print(f"📡 Téléchargement {i+1}/{len(assets)} : {asset}")
        data = yf.download(asset, period="max")
        if not data.empty:
            data.to_sql(asset, con=engine, if_exists="replace", index=True)
    except Exception as e:
        print(f"⚠️ Erreur avec {asset} : {e}")
    
    time.sleep(1)  # ⏳ Pause pour éviter un blocage par Yahoo Finance

print("✅ Toutes les données ont été enregistrées en base SQL !")
