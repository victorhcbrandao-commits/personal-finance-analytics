from src.load_data import carregar_transacoes
from src.clean_data import limpar_transacoes
from src.analysis import (
    calcular_receitas,
    calcular_despesas,
    calcular_saldo,
    gastos_por_categoria,
    maiores_despesas        
)


df = carregar_transacoes(
    "data/raw/transacoes.csv"
)

df = limpar_transacoes(df)


receitas = calcular_receitas(df)

despesas = calcular_despesas(df)

saldo = calcular_saldo(df)


categorias = gastos_por_categoria(df)

top_despesas = maiores_despesas(df)


print(f"Receitas: R$ {receitas:.2f}")

print(f"Despesas: R$ {despesas:.2f}")

print (f"Saldo: R$ {saldo:.2f}")

print()
print("Gastos por categoria:")
print(categorias)

print()
print("Top maiores despesas:")
print(top_despesas)



