import streamlit as st
import plotly.express as px

from src.load_data import carregar_transacoes
from src.clean_data import limpar_transacoes
from src.cashflow import (
    gerar_fluxo_caixa,
    gerar_resumo_mensal
)
from src.analysis import maiores_despesas
from src.analysis import gastos_por_categoria
from src.analysis import (
    maiores_despesas,
    maiores_receitas,
    gastos_por_categoria
)

st.title(
    "FinSight - Personal Finance Analytics"
)

df = carregar_transacoes("data/raw/transacoes.csv")

df = limpar_transacoes(df)

st.sidebar.title(
    "Filtros"
)

meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

meses_invertido = {
    valor: chave
    for chave, valor in meses.items()
}

anos = sorted(df["data_compra"].dt.year.unique())

ano_selecionado = st.sidebar.selectbox(
    "Ano",
    anos
)

df = df[
    df["data_compra"].dt.year == ano_selecionado
]  

meses_disponiveis = sorted(
    df["data_compra"].dt.month.unique()
)

nomes_meses = [
    meses[mes]
    for mes in meses_disponiveis
]

mes_selecionado = st.sidebar.selectbox(
    "Mês",
    ["Todos"] + nomes_meses
)

if mes_selecionado != "Todos":

    numero_mes = meses_invertido[
        mes_selecionado
    ]

    df = df[
        df["data_compra"].dt.month == numero_mes
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

top_receitas = maiores_receitas(df)

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
    top_despesas,
    hide_index=True
)

st.subheader(
    "Top Receitas"
)

st.dataframe(
    top_receitas,
    hide_index=True
)

st.subheader(
    "Gastos por Categoria"
)

st.dataframe(
    categorias,
    hide_index=True
)

st.bar_chart(
    categorias.set_index("categoria")["valor"]
)

st.subheader(
    "Distribuição dos Gastos"
)

df_pizza = categorias.reset_index()

df_pizza["percentual"] = (
    df_pizza["valor"]
    / df_pizza["valor"].sum()
    * 100
)

df_pizza["texto"] = df_pizza["percentual"].apply(
    lambda x: f"{x:.1f}%" if x >= 5 else ""
)

valor_total = (
    f"R$ {df_pizza['valor'].sum():,.2f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

fig = px.pie(
    df_pizza,
    names="categoria",
    values="valor",
    hole=0.65
)

fig.update_traces(
    text=df_pizza["texto"],
    textinfo="text",
    textposition="inside"
)

fig.update_layout(
    showlegend=True,

    legend=dict(
        x=0.83,
        y=0.95
    ),

    margin=dict(
        t=20,
        b=20,
        l=20,
        r=20
    ),

    annotations=[
        dict(
            text=f"{valor_total}<br>Despesas",
            x=0.5,
            y=0.5,
            font_size=22,
            showarrow=False
        )
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

df_exibicao = df[
    [
        "data_compra",
        "descricao",
        "categoria",
        "tipo_pagamento",
        "valor"
    ]
].copy()


df_exibicao["data_compra"] = (
    df_exibicao["data_compra"]
    .dt.strftime("%d/%m/%Y")
)

df_exibicao.columns = [
    "Data",
    "Descrição",
    "Categoria",
    "Tipo de Pagamento",
    "Valor"
]

df_exibicao["Valor"] = (
    df_exibicao["Valor"]
    .apply(
        lambda x:
        f"R$ {x:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
)

st.subheader(
    "Transações"
)

st.dataframe(
    df_exibicao
)