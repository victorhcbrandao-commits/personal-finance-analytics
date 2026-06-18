import pandas as pd

from datetime import datetime

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
from src.cards import gerar_parcelas
from src.cashflow import gerar_fluxo_caixa
from src.cashflow import (
    gerar_fluxo_caixa,
    gerar_resumo_mensal
)



df = carregar_transacoes(
    "data/raw/transacoes.csv"
)

df = limpar_transacoes(df)

df_fluxo_caixa = gerar_fluxo_caixa(df)

df_resumo_mensal = gerar_resumo_mensal(
    df_fluxo_caixa
)


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
print("Sistema de Parcelamento")

parcelas_notebook = gerar_parcelas(
    "Notebook Dell",
    3600,
    10,
    datetime(
        2026,
        1,
        10
    ),
    "Black Visa"
)

df_parcelas = pd.DataFrame(parcelas_notebook)

df_fluxo_caixa = gerar_fluxo_caixa(df)

print()
print("Fluxo de Caixa Projetado")
print(df_fluxo_caixa)

print()
print("Resumo Mensal")

print(df_resumo_mensal)

