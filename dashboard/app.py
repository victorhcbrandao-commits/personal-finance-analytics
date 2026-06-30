# ==============================================================================
# 1. IMPORTS
# ==============================================================================

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

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

from pages.dashboard_sections.patrimonio import renderizar_patrimonio

from pages.dashboard_sections.saldo_projetado import renderizar_saldo_projetado

from pages.dashboard_sections.fluxo_caixa import renderizar_fluxo_caixa

from pages.dashboard_sections.gastos import renderizar_gastos

from pages.dashboard_sections.transacoes import renderizar_transacoes

from pages.dashboard_sections.cartoes import renderizar_cartoes

from pages.dashboard_sections.planejamento import renderizar_planejamento

from pages.dashboard_sections.projecoes import renderizar_projecoes

from pages.dashboard_sections.renda_passiva import renderizar_renda_passiva

from pages.dashboard_sections.fire import renderizar_fire


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

st.divider()


# ==============================================================================
# 6.DASHBOARD
# ==============================================================================



# ------------------------------------------------------------------------------
# 6.1 PATRIMÔNIO
# ------------------------------------------------------------------------------

renderizar_patrimonio(
    patrimonio,
    caixa,
    investimentos,
    patrimonio_instituicao,
    patrimonio_tipo,
    df_historico_filtrado
)

st.divider()


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

st.divider()

# ------------------------------------------------------------------------------
# 6.3 SALDO MENSAL PROJETADO
# ------------------------------------------------------------------------------


renderizar_saldo_projetado(
    df_resumo_mensal
)

st.divider()

# ------------------------------------------------------------------------------
# 6.4 FLUXO DE CAIXA
# ------------------------------------------------------------------------------


renderizar_fluxo_caixa(
    df_resumo_mensal
)

st.divider()


# ------------------------------------------------------------------------------
# 6.5 GASTOS E DESPESAS
# ------------------------------------------------------------------------------


renderizar_gastos(
    top_despesas,
    top_receitas,
    categorias,
    cartoes
)

st.divider()

# ------------------------------------------------------------------------------
# 6.6 TABELA DE TRANSAÇÕES E EXPORTAÇÃO
# ------------------------------------------------------------------------------

renderizar_transacoes(df)


# ------------------------------------------------------------------------------
# 6.7 CARTÕES
# ------------------------------------------------------------------------------


renderizar_cartoes(
    faturas_filtrado,
    formatar_moeda
)


# ------------------------------------------------------------------------------
# 6.8 PLANEJAMENTO
# ------------------------------------------------------------------------------

renderizar_planejamento(
    df_projecao,
    df_metas,
    patrimonio,
    aporte_mensal,
    calcular_meses_meta
)
        

# ------------------------------------------------------------------------------
# 6.9 PROJEÇÕES
# ------------------------------------------------------------------------------


renderizar_projecoes(
    df_projecao
)


# ------------------------------------------------------------------------------
# 6.10 RENDA PASSIVA
# ------------------------------------------------------------------------------


renderizar_renda_passiva(
    renda_passiva,
    df_dividendos_mes,
    df_dividendos_filtrado
)

# ------------------------------------------------------------------------------
# 6.11 INDEPENDÊNCIA FINANCEIRA (FIRE)
# ------------------------------------------------------------------------------


renderizar_fire(
    patrimonio_objetivo,
    percentual_independencia,
    anos_faltantes,
    formatar_moeda
)