from src.load_data import carregar_transacoes
from src.clean_data import limpar_transacoes
from src.analysis import (
    calcular_receitas,
    calcular_despesas,
    calcular_saldo,
    gastos_por_categoria,
    maiores_despesas        
)
from src.cards import (
    obter_dia_fechamento,
    obter_dia_vencimento
)
from src.cards import (
    obter_dia_fechamento,
    obter_dia_vencimento,
    calcular_fatura
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

print()
print("Teste dos cartões")

print(
    obter_dia_fechamento(
        "Black Master"
    )
)

print(
    obter_dia_vencimento(
        "Black Master"
    )
)

from datetime import datetime

print()
print("Teste das Faturas")

data_compra = datetime(
    2026,
    12,
    20
)

fatura = calcular_fatura(
    data_compra,
    "Black Master"
)

print(fatura)



