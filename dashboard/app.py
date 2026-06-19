import streamlit as st

from src.load_data import carregar_transacoes
from src.clean_data import limpar_transacoes
from src.cashflow import (
    gerar_fluxo_caixa,
    gerar_resumo_mensal
)
from src.analysis import maiores_despesas
from src.analysis import gastos_por_categoria

st.title(
    "FinSight - Personal Finance Analytics"
)

df = carregar_transacoes("data/raw/transacoes.csv")

df = limpar_transacoes(df)

st.sidebar.title(
    "Filtros"
)
anos = sorted(df["data_compra"].dt.year.unique())

ano_selecionado = st.sidebar.selectbox(
    "Ano",
    anos
)

df = df[
    df["data_compra"].dt.year == ano_selecionado
]    

categorias = sorted(
    df["categoria"].unique()
)

categoria_selecionada = st.sidebar.selectbox(
    "Categoria",
    ["Todas"] + categorias
)

if categoria_selecionada != "Todas":
    
    df = df[
    df["categoria"] == categoria_selecionada
]

tipo_pagamento_selecionado = st.sidebar.selectbox(
    "Tipo de Pagamento",
    ["Todos"] + sorted(df["tipo_pagamento"].unique())
)
if tipo_pagamento_selecionado != "Todos":

    df = df[
        df["tipo_pagamento"] == tipo_pagamento_selecionado
    ]

top_despesas = maiores_despesas(df)

categorias = gastos_por_categoria(df)

df_fluxo_caixa = gerar_fluxo_caixa(df)

df_resumo_mensal = gerar_resumo_mensal(
    df_fluxo_caixa
)

df_resumo_mensal["periodo"] = (
    df_resumo_mensal["ano"].astype(str)
    + "-"
    + df_resumo_mensal["mes"].astype(str).str.zfill(2)
)

total_receitas = df_resumo_mensal["Receita"].sum()

total_despesas = df_resumo_mensal["Despesa"].sum()

saldo_acumulado = df_resumo_mensal["Saldo"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Receitas",
    f"R$ {total_receitas:.2f}"
)

col2.metric(
    "Despesas",
    f"R$ {total_despesas:.2f}"
)

col3.metric(
    "Saldo",
    f"R$ {saldo_acumulado:.2f}"
)

st.subheader("Saldo Mensal Projetado")

st.line_chart(
    df_resumo_mensal,
    x="periodo",
    y="Saldo"
)

st.subheader(
    "Top Maiores Despesas"
)

st.dataframe(
    top_despesas
)

st.subheader(
    "Gastos por Categoria"
)

st.dataframe(
    categorias
)

st.bar_chart(
    categorias
)