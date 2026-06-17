from src.load_data import carregar_transacoes
from src.clean_data import limpar_transacoes


df = carregar_transacoes(
    "data/raw/transacoes.csv"
    )


print(df.head())

print()

df.info()

