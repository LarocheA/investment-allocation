import pandas as pd

def load_data():
    # Charger les fichiers CSV dans des DataFrames pandas.
    cac_stocks = pd.read_csv("data/cac_stocks.csv")
    crypto_list = pd.read_csv("data/crypto_list.csv")
    europe_stocks = pd.read_csv("data/europe_stocks.csv", delimiter=";")
    hongkong_stocks = pd.read_csv("data/hongkong_stocks.csv")
    japan_stocks = pd.read_csv("data/japan_stocks.csv")
    scpi_list = pd.read_csv("data/scpi_list.csv")

    return {
        "cac_stocks": cac_stocks,
        "crypto_list": crypto_list,
        "europe_stocks": europe_stocks,
        "hongkong_stocks": hongkong_stocks,
        "japan_stocks": japan_stocks,
        "scpi_list": scpi_list,
    }

if __name__ == "__main__":
    data = load_data()
    
    # Afficher un aperçu des données.
    for name, df in data.items():
        print(f"\n{name}:\n", df.head())
