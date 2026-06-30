# ==============================================================================
# 1. IMPORTS
# ==============================================================================

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from math import ceil


from io import BytesIO


from components.graficos import(
    grafico_patrimonio_instituicao,
    grafico_patrimonio_tipo,
    grafico_evolucao_patrimonial,
    grafico_projecao,
    grafico_dividendos
)
from components.card_fire import card_fire
from components.card_meta import card_meta
from components.card_cartao import card_cartao
from components.card_kpi import card_kpi
from src.utils import formatar_moeda
from src.load_data import (
    carregar_transacoes,
    carregar_cartoes,
    carregar_patrimonio,
    carregar_patrimonio_historico,
    carregar_metas,
    carregar_projecao,
    carregar_renda_passiva
)

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
    gastos_por_categoria,
    despesas_por_cartao,
    proximas_faturas,
    patrimonio_total,
    caixa_total,
    investimentos_total,
    patrimonio_por_instituicao,
    patrimonio_por_tipo,
    calcular_meses_meta,
    renda_passiva_total,
    dividendos_por_mes,
    patrimonio_fire,
    percentual_fire,
    anos_para_fire,
    taxa_economia,
    renda_passiva_anual,
    dividend_yield,
    crescimento_patrimonial_mensal,
    meses_reserva_financeira,
    crescimento_patrimonial_anual
    )

from src.indicadores import calcular_variacao_receita, calcular_variacao_despesa

from pages.dashboard_sections.overview import renderizar_visao_geral

# ==============================================================================
# 2. CONFIGURAÇÃO DA APLICAÇÃO
# ==============================================================================


st.title(
    "FinSight"
)

st.caption(
    "Panorama completo da sua vida financeira"
)


# ==============================================================================
# 3. CARREGAMENTO DOS DADOS
# ==============================================================================

df = carregar_transacoes("data/raw/transacoes.csv")

df_cartoes = carregar_cartoes("data/raw/cartoes.csv")


df_patrimonio = carregar_patrimonio("data/raw/patrimonio.csv")

patrimonio = patrimonio_total(
    df_patrimonio
)

faturas = proximas_faturas(df, df_cartoes)


df_patrimonio_historico = carregar_patrimonio_historico("data/raw/patrimonio_historico.csv")


df_metas = carregar_metas("data/raw/metas.csv")

df_projecao = carregar_projecao("data/raw/projecao.csv")

df_projecao["saldo"] = (
    df_projecao["receita"]
    - df_projecao["despesa"]
)

df_projecao["saldo_acumulado"] = (
    df_projecao["saldo"]
    .cumsum()
)

df_projecao["patrimonio_projetado"] = (
    patrimonio
    + df_projecao["saldo_acumulado"]
)


df_metas["percentual"] = (
    df_metas["atual"]
    / df_metas["objetivo"]
) * 100


df_renda_passiva = carregar_renda_passiva("data/raw/renda_passiva.csv")

renda_passiva = renda_passiva_total(
    df_renda_passiva
)

renda_passiva_ano = (
    renda_passiva_anual(
        renda_passiva
    )
)

dividend_yield_percentual = (
    dividend_yield(
        renda_passiva_ano,
        patrimonio
    )
)

crescimento_patrimonio_percentual = crescimento_patrimonial_mensal(
    df_patrimonio_historico
)

crescimento_anual = (
    crescimento_patrimonial_anual(
        df_patrimonio_historico
    )
)


# ==============================================================================
# 4. SIDEBAR E FILTROS
# ==============================================================================


st.sidebar.title(
    "Filtros"
)

st.sidebar.markdown(
    "Use os filtros abaixo para analisar os dados."
)

filtro_instituicao = st.sidebar.selectbox(
    "Instituição",
    ["Todas"] + sorted(
        df_patrimonio["instituicao"].unique()
    )
)

df_patrimonio_filtrado = df_patrimonio.copy()

if filtro_instituicao != "Todas":

    df_patrimonio_filtrado = (
        df_patrimonio_filtrado[
            df_patrimonio_filtrado["instituicao"]
            == filtro_instituicao
        ]
    )

    
filtro_tipo_patrimonio = st.sidebar.selectbox(
    "Tipo de Patrimônio",
    ["Todos"] + sorted(
        df_patrimonio["tipo"].unique()
    )
)

if filtro_tipo_patrimonio != "Todos":

    df_patrimonio_filtrado = (
        df_patrimonio_filtrado[
            df_patrimonio_filtrado["tipo"]
            == filtro_tipo_patrimonio
        ]
    )

filtro_cartao = st.sidebar.selectbox(
    "Cartão",
    ["Todos"] + sorted(
        df_cartoes["cartao"].unique()
    )
)

df_cartoes_filtrado = df_cartoes.copy()

if filtro_cartao != "Todos":

    df_cartoes_filtrado = (
        df_cartoes_filtrado[
            df_cartoes_filtrado["cartao"]
            == filtro_cartao
        ]
    )

faturas_filtrado = faturas.copy()

if filtro_cartao != "Todos":
    faturas_filtrado = faturas_filtrado[
        faturas_filtrado["cartao"] == filtro_cartao
    ]


patrimonio = patrimonio_total(
    df_patrimonio_filtrado
)

filtro_periodo = st.sidebar.selectbox(
    "Período",
    [
        "Tudo",
        "Último mês",
        "Últimos 3 meses",
        "Últimos 6 meses",
        "Ano atual"
    ]
)

df = limpar_transacoes(df)

df_historico_filtrado = (
    df_patrimonio_historico.copy()
)

if filtro_periodo == "Último mês":

    df_historico_filtrado = (
        df_historico_filtrado.tail(1)
    )

elif filtro_periodo == "Últimos 3 meses":

    df_historico_filtrado = (
        df_historico_filtrado.tail(3)
    )

elif filtro_periodo == "Últimos 6 meses":

    df_historico_filtrado = (
        df_historico_filtrado.tail(6)
    )

elif filtro_periodo == "Ano atual":

    ano_atual = (
        df_historico_filtrado["data"]
        .dt.year
        .max()
    )

    df_historico_filtrado = (
        df_historico_filtrado[
            df_historico_filtrado["data"].dt.year
            == ano_atual
        ]
    )

df_dividendos_mes = dividendos_por_mes(
    df_renda_passiva
)

df_dividendos_filtrado = (
    df_dividendos_mes.copy()
)

if filtro_periodo == "Último mês":

    df_dividendos_filtrado = (
        df_dividendos_filtrado.tail(1)
    )

elif filtro_periodo == "Últimos 3 meses":

    df_dividendos_filtrado = (
        df_dividendos_filtrado.tail(3)
    )

elif filtro_periodo == "Últimos 6 meses":

    df_dividendos_filtrado = (
        df_dividendos_filtrado.tail(6)
    )

df_projecao_filtrado = (
    df_projecao.copy()
)

if filtro_periodo == "Último mês":

    df_projecao_filtrado = (
        df_projecao_filtrado.tail(1)
    )

elif filtro_periodo == "Últimos 3 meses":

    df_projecao_filtrado = (
        df_projecao_filtrado.tail(3)
    )

elif filtro_periodo == "Últimos 6 meses":

    df_projecao_filtrado = (
        df_projecao_filtrado.tail(6)
    )


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


# ==============================================================================
# 5. PROCESSAMENTO DOS DADOS
# ==============================================================================


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
    .apply(formatar_moeda)
)

categorias = gastos_por_categoria(df)

cartoes = despesas_por_cartao(df)

cartoes["valor_formatado"] = (
    cartoes["valor"]
    .apply(formatar_moeda)
)

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

taxa_economia_percentual = (
    taxa_economia(
        total_receitas,
        total_despesas
    )
)

patrimonio_geral = patrimonio_total(
    df_patrimonio
)

df_patrimonio_filtrado = df_patrimonio.copy()

meses_reserva = meses_reserva_financeira(
    patrimonio_geral,
    total_despesas
)

patrimonio = patrimonio_total(
    df_patrimonio_filtrado
)

caixa = caixa_total(
    df_patrimonio_filtrado
)

investimentos = investimentos_total(
    df_patrimonio_filtrado
)

aporte_mensal = (
    total_receitas
    - total_despesas
)

despesa_anual = (
    total_despesas
    * 12
)

patrimonio_objetivo = patrimonio_fire(
    despesa_anual
)

percentual_independencia = percentual_fire(
    patrimonio,
    patrimonio_objetivo
)

aporte_anual = (
    aporte_mensal
    * 12
)

anos_faltantes = anos_para_fire(
    patrimonio,
    patrimonio_objetivo,
    aporte_anual
)



meses_reserva_meta = calcular_meses_meta(
    50000,
    patrimonio,
    aporte_mensal
)

meses_computador = calcular_meses_meta(
    12000,
    patrimonio,
    aporte_mensal
)

meses_viagem = calcular_meses_meta(
    30000,
    patrimonio,
    aporte_mensal
)

meses_apartamento = calcular_meses_meta(
    150000,
    patrimonio,
    aporte_mensal
)

patrimonio_instituicao = (
    patrimonio_por_instituicao(
        df_patrimonio_filtrado
    )
)

patrimonio_tipo = (
    patrimonio_por_tipo(
        df_patrimonio_filtrado
    )
)

# TODO: Substituir pelo valor do período anterior quando tivermos histórico

receita_atual = total_receitas
receita_anterior = 7800  # temporário para teste


variacao_receita = calcular_variacao_receita(
    receita_atual,
    receita_anterior
)

despesa_atual = total_despesas
despesa_anterior = 4200

variacao_despesa = calcular_variacao_despesa(
    despesa_atual,
    despesa_anterior
)



# ==============================================================================
# 6.DASHBOARD
# ==============================================================================

# ------------------------------------------------------------------------------
# 6.1 PATRIMÔNIO
# ------------------------------------------------------------------------------


st.divider()

st.header(
    "💰 Patrimônio"
)

col1, col2, col3 = st.columns(3)

with col1:
    card_kpi(
        "Patrimônio Total",
        formatar_moeda(patrimonio),
        "💰",
        "#3B82F6"
    )

with col2:
    card_kpi(
        "Caixa",
        formatar_moeda(caixa),
        "💵",
        "#00CC96"
    )

with col3:
    card_kpi(
        "Investimentos",
        formatar_moeda(investimentos),
        "📈",
        "#F59E0B"
    )


st.subheader(
    "Patrimônio por Instituição"
)

patrimonio_instituicao["valor_formatado"] = (
    patrimonio_instituicao["valor"]
    .apply(formatar_moeda)
)

grafico_patrimonio_instituicao(
    patrimonio_instituicao
)

st.subheader(
    "Patrimônio por Tipo"
)

patrimonio_tipo["valor_formatado"] = (
    patrimonio_tipo["valor"]
    .apply(formatar_moeda)
)

grafico_patrimonio_tipo(
    patrimonio_tipo
)


st.subheader(
    "Evolução Patrimonial"
)

grafico_evolucao_patrimonial(
    df_historico_filtrado
)

# ------------------------------------------------------------------------------
# 6.2 VISÃO GERAL
# ------------------------------------------------------------------------------

renderizar_visao_geral(
    total_receitas,
    total_despesas,
    saldo_acumulado,
    taxa_economia_percentual,
    crescimento_patrimonio_percentual,
    crescimento_anual,
    renda_passiva,
    meses_reserva,
    percentual_independencia,
    variacao_receita,
    variacao_despesa
)


# ------------------------------------------------------------------------------
# 6.3 SALDO MENSAL PROJETADO
# ------------------------------------------------------------------------------


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
    width="stretch",
    config={
        "displayModeBar": False
    }
)

# ------------------------------------------------------------------------------
# 6.4 FLUXO DE CAIXA
# ------------------------------------------------------------------------------


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
            color="#3B82F6",
            width=5
        ),
        marker=dict(
            size=9,
            color="#93C5FD",
            line=dict(
                width=2,
                color="#3B82F6"
            )
        )
    )
)

fig.update_xaxes(
    title_text=None,
    showgrid=False
)

fig.update_yaxes(
    title_text=None,
    showgrid=True,
    gridcolor="#1f2937"
)

fig.update_layout(
    template="plotly_dark",
    barmode="group",
    xaxis_title=None,
    yaxis_title=None,
    height=500,
    hovermode="x unified",
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#F8FAFC",
        size=12
    ),
    legend=dict(
        orientation="h",
        x=0,
        y=1.12
    ),
    bargap=0.35
)

st.subheader("Fluxo de Caixa Mensal")

st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)


# ------------------------------------------------------------------------------
# 6.5 GASTOS E DESPESAS
# ------------------------------------------------------------------------------


st.subheader("Top Maiores Despesas")

fig = px.bar(
    top_despesas,
    x="valor",
    y="descricao",
    orientation="h",
    text="valor_formatado",
    color_discrete_sequence=["#EF553B"]
)

fig.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    textfont=dict(
        size=13,
        color="white"
    ),
    marker=dict(
        color="#EF553B",
        line=dict(width=0)
    )
)

fig.update_xaxes(
    range=[0, top_despesas["valor"].max() * 1.45],
    visible=False,
    showgrid=False
)

fig.update_yaxes(
    title="",
    showgrid=False
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    },
    height=420,
    margin=dict(l=20, r=100, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#F8FAFC",
        size=12
    ),
    bargap=0.25
)

st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)

st.subheader("Top Receitas")

fig = px.bar(
    top_receitas,
    x="valor",
    y="descricao",
    orientation="h",
    text="valor_formatado",
    color_discrete_sequence=["#00CC96"]
)

fig.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    textfont=dict(
        size=13,
        color="white"
    ),
    marker=dict(
        color="#00CC96",
        line=dict(width=0)
    )
)

fig.update_xaxes(
    range=[0, top_receitas["valor"].max() * 1.35],
    visible=False,
    showgrid=False
)

fig.update_yaxes(
    title="",
    showgrid=False
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    },
    height=280,
    margin=dict(l=20, r=100, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#F8FAFC",
        size=12
    ),
    bargap=0.25
)

st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)

st.subheader("Gastos por Categoria")

categorias_exibir = categorias.copy()

categorias_exibir["valor"] = (
    categorias_exibir["valor"]
    .apply(formatar_moeda)
)

categorias_exibir = categorias_exibir.rename(
    columns={
        "categoria": "Categoria",
        "valor": "Valor"
    }
)

st.dataframe(
    categorias_exibir,
    hide_index=True,
    width="stretch"
)

fig = px.bar(
    categorias,
    x="categoria",
    y="valor",
    text="valor",
    color_discrete_sequence=["#EF553B"]
)

fig.update_traces(
    texttemplate="R$ %{text:.2f}",
    textposition="outside",
    textfont=dict(
        size=13,
        color="white"
    ),
    marker=dict(
        color="#EF553B",
        line=dict(width=0)
    )
)

fig.update_yaxes(
    title="",
    showgrid=True,
    gridcolor="#1f2937"
)

fig.update_xaxes(
    title="",
    showgrid=False
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    height=420,
    margin=dict(l=20, r=40, t=20, b=40),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#F8FAFC",
        size=12
    ),
    bargap=0.35
)

st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)

st.subheader("Despesas por Cartão")

fig = px.bar(
    cartoes,
    x="valor",
    y="cartao",
    orientation="h",
    text="valor_formatado",
    color="cartao",
    color_discrete_map={
        "Black Visa": "#F59E0B",
        "Black Master": "#EF4444",
        "Azul Platinum": "#2563EB"
    }
)

fig.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    textfont=dict(
        size=13,
        color="white"
    ),
    marker=dict(
        line=dict(width=0)
    )
)

fig.update_xaxes(
    range=[0, cartoes["valor"].max() * 1.45],
    visible=False,
    showgrid=False
)

fig.update_yaxes(
    title="",
    showgrid=False
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    },
    height=420,
    margin=dict(l=20, r=100, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#F8FAFC",
        size=12
    ),
    bargap=0.25
)

st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)


st.subheader("Distribuição dos Gastos")

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
    hole=0.72,
    color_discrete_sequence=[
        "#3B82F6",
        "#00CC96",
        "#F59E0B",
        "#EF553B",
        "#8B5CF6",
        "#EC4899"
    ]
)

fig.update_traces(
    text=df_pizza["texto"],
    textinfo="text",
    textposition="inside",
    textfont=dict(
        size=14,
        color="white"
    ),
    marker=dict(
        line=dict(
            color="#111827",
            width=2
        )
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#F8FAFC",
        size=12
    ),
    showlegend=True,
    legend=dict(
        x=1.02,
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
            text=f"<b>{valor_total}</b><br>Despesas",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(
                size=24,
                color="white"
            )
        )
    ]
)

st.plotly_chart(
    fig,
    width="stretch",
    config={
        "displayModeBar": False
    }
)

# ------------------------------------------------------------------------------
# 6.6 TABELA DE TRANSAÇÕES E EXPORTAÇÃO
# ------------------------------------------------------------------------------



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

st.divider()

# ------------------------------------------------------------------------------
# 6.7 CARTÕES
# ------------------------------------------------------------------------------


st.header(
    "💳 Cartões"
)

st.subheader(
    "Próximas Faturas"
)

col1, col2, col3 = st.columns(3)

for i, (_, linha) in enumerate(faturas_filtrado.iterrows()):

    coluna = [col1, col2, col3][i % 3]

    with coluna:
        card_cartao(
            linha,
            formatar_moeda
        )

st.divider()


# ------------------------------------------------------------------------------
# 6.8 PLANEJAMENTO
# ------------------------------------------------------------------------------



st.header(
    "🎯 Planejamento"
)

patrimonio_dezembro = (
    df_projecao["patrimonio_projetado"]
    .iloc[-1]
)

col1, col2 = st.columns(2)

with col1:

    card_kpi(
        "Patrimônio Projetado",
        formatar_moeda(
            patrimonio_dezembro
        ),
        "🚀",
        "#3B82F6"
    )

with col2:

    crescimento = (patrimonio_dezembro - patrimonio)

    card_kpi(
        "Crescimento Projetado",
        formatar_moeda(
            crescimento
        ),
        "📈",
        "#00CC96"
    )
        

st.subheader(
    "Metas Financeiras"
)

col1, col2 = st.columns(2)


for i, (_, linha) in enumerate(df_metas.iterrows()):

    
    coluna = [col1, col2][i % 2]

    
    with coluna:

        card_meta(
            linha,
            patrimonio,
            aporte_mensal,
            formatar_moeda,
            calcular_meses_meta
        )
        
st.divider()


# ------------------------------------------------------------------------------
# 6.9 PROJEÇÕES
# ------------------------------------------------------------------------------


st.header(
    "📈 Projeções"
)

st.subheader(
    "Projeção Financeira"
)

grafico_projecao(
    df_projecao
)

st.divider()


# ------------------------------------------------------------------------------
# 6.10 RENDA PASSIVA
# ------------------------------------------------------------------------------


st.header(
    "💵 Renda Passiva"
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    card_kpi(
        "Renda Passiva Total",
        formatar_moeda(renda_passiva),
        "💵",
        "#00CC96"
    )

with col2:
    media_mensal = df_dividendos_mes["valor"].mean()

    card_kpi(
        "Média Mensal",
        formatar_moeda(media_mensal),
        "📈",
        "#3B82F6"
    )


st.divider()


st.subheader(
    "📈 Dividendos por Mês"
)

df_dividendos_filtrado["valor_formatado"] = (
    df_dividendos_filtrado["valor"]
    .apply(formatar_moeda)
)

grafico_dividendos(
    df_dividendos_filtrado
)

st.divider()

# ------------------------------------------------------------------------------
# 6.11 INDEPENDÊNCIA FINANCEIRA (FIRE)
# ------------------------------------------------------------------------------


st.header(
    "🔥 Independência Financeira"
)

col1, col2, col3 = st.columns(3)

card_fire(
    patrimonio_objetivo,
    percentual_independencia,
    anos_faltantes,
    formatar_moeda
)