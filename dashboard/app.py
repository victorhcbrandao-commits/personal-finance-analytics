import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


from io import BytesIO

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

st.caption(
    "Panorama completo da sua vida financeira"
)

df = carregar_transacoes("data/raw/transacoes.csv")

df = limpar_transacoes(df)

st.sidebar.title(
    "FinSight"
)

pagina = st.sidebar.radio(
    "Menu",
    [
        "🏠 Visão Geral",
        "📈 Fluxo de Caixa",
        "💳 Cartões de Crédito",
        "📅 Planejamento",
        "🎯 Metas",
        "📊 Relatórios",
        "⚙️ Configurações"
    ]
)

st.sidebar.divider()

st.sidebar.subheader(
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

top_despesas["valor_formatado"] = (
    top_despesas["valor"]
    .apply(
        lambda x:
        f"R$ {x:,.0f}"
        .replace(",", ".")
        if x.is_integer()
        else
        f"R$ {x:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
)

top_receitas = maiores_receitas(df)

top_receitas["valor_formatado"] = (
    top_receitas["valor"]
    .apply(
        lambda x:
        f"R$ {x:,.0f}"
        .replace(",", ".")
        if x.is_integer()
        else
        f"R$ {x:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
)

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

quantidade_transacoes= len(df)

def formatar_moeda(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

def card_kpi(titulo, valor, icone, cor):

    st.markdown(
        f"""
<div style='background-color:#111827; padding:20px; border-radius:16px; border:1px solid #1f2937; min-height:120px;'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <span style='font-size:16px; color:#cbd5e1;'>{titulo}</span>
        <span style='font-size:20px;'>{icone}</span>
    </div>
    <div style='font-size:24px; font-weight:700; color:{cor}; margin-top:18px; white-space:nowrap;'>
        {valor}
    </div>
</div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    card_kpi("Receitas", formatar_moeda(total_receitas), "💰", "#00CC96")

with col2:
    card_kpi("Despesas", formatar_moeda(total_despesas), "📉", "#EF553B")

with col3:
    card_kpi("Saldo", formatar_moeda(saldo_acumulado), "💳", "#636EFA")

with col4:
    card_kpi("Transações", quantidade_transacoes, "📊", "#FFFFFF")

st.subheader(
    "Saldo Mensal Projetado"
)

fig = px.line(
    df_resumo_mensal,
    x="periodo",
    y="Saldo",
    markers=True
)

fig.update_layout(
    xaxis_title="Período",
    yaxis_title="Valor",
    legend_title="Tipo"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

df_grafico = df_resumo_mensal.copy()

df_grafico["Saldo Acumulado"] = (
    df_grafico["Saldo"].cumsum()
)


fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df_grafico["periodo"],
        y=df_grafico["Receita"],
        name="Receitas",
        marker_color="#00CC96"
    )
)

fig.add_trace(
    go.Bar(
        x=df_grafico["periodo"],
        y=df_grafico["Despesa"],
        name="Despesas",
        marker_color="#EF553B"
    )
)

fig.add_trace(
    go.Scatter(
        x=df_grafico["periodo"],
        y=df_grafico["Saldo Acumulado"],
        mode="lines+markers",
        name="Saldo Acumulado",
        line=dict(
            color="#636EFA",
            width=3
        ),
        marker=dict(size=8)
    )
)

fig.update_layout(

    barmode="group",

    xaxis_title="",

    yaxis_title="",

    template="plotly_dark",

    height=500,

    hovermode="x unified",

    legend=dict(
        orientation="h",
        x=0,
        y=1.10
    )
)

st.subheader(
    "Fluxo de Caixa Mensal"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Top Maiores Despesas"
)


fig = px.bar(
    top_despesas,
    x="valor",
    y="descricao",
    orientation="h",
    text="valor"
)

fig.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    }
)

fig.update_traces(
    text=top_despesas["valor_formatado"],
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Valor (R$)",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    }
)

fig.update_xaxes(
    range=[0, top_despesas["valor"].max() * 1.25]
)

fig.update_xaxes(
    visible=False
)

fig.update_layout(
    xaxis_title="Valor (R$)",
    yaxis_title="",
    showlegend=False
)

fig.update_layout(
    xaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Top Receitas"
)

fig = px.bar(
    top_receitas,
    x="valor",
    y="descricao",
    orientation="h",
    text="valor_formatado",
    color_discrete_sequence=["#00CC96"]
)

fig.update_traces(
    textposition="outside"
)

fig.update_xaxes(
    range=[0, top_receitas["valor"].max() * 1.25],
    visible=False
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Gastos por Categoria"
)

st.dataframe(
    categorias,
    hide_index=True
)

fig = px.bar(
    categorias,
    x="categoria",
    y="valor",
    text="valor"
)

fig.update_layout(
    xaxis_title="Categoria",
    yaxis_title="Valor",
    showlegend=False
)

fig.update_traces(
    texttemplate="R$ %{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
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

buffer = BytesIO()

df_exibicao.to_excel(
    buffer,
    index=False,
    engine="openpyxl"
)

buffer.seek(0)

st.download_button(
    label="📥 Baixar Transações em Excel",
    data=buffer,
    file_name="transacoes.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

excel = df_exibicao.to_excel(
    "transacoes.xlsx",
    index=False
)

st.subheader(
    "Transações"
)

st.dataframe(
    df_exibicao
)