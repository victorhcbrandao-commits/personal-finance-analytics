from src.load_data import carregar_transacoes

df = carregar_transacoes(
    "data/raw/transacoes.csv"
    )

print(df.head())

print()

df.info()

