import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Charger la clé API depuis le fichier .env
load_dotenv()
api_key = os.getenv("COINMARKETCAP_API_KEY")

# URL de l'API CoinMarketCap
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Paramètres pour récupérer un max de cryptos
params = {
    "start": 1,  # Commence à la première crypto
    "limit": 5000,  # Récupère les 5000 premières cryptos
    "convert": "USD"
}

# En-têtes avec clé API
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": api_key,
}

# Requête API
response = requests.get(url, headers=headers, params=params)
data = response.json()

# Extraire les données utiles
crypto_list = []
for crypto in data["data"]:
    crypto_list.append({
        "Symbol": crypto["symbol"],
        "Name": crypto["name"],
        "Price": crypto["quote"]["USD"]["price"]
    })

# 📂 Sauvegarder en CSV
df = pd.DataFrame(crypto_list)
df.to_csv("data/crypto_list.csv", index=False)

print("Liste des cryptos enregistrée !")
