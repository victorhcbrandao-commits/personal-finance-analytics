"""
==============================================================================
FinSight
Módulo: Visão Geral

Responsável pela renderização da visão geral do dashboard.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from components.card_kpi import card_kpi
from src.utils import formatar_moeda


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================


def renderizar_visao_geral(
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
):    
   
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card_kpi(
            "Receitas",
            formatar_moeda(total_receitas),
            "💰",
            "#00CC96",
            "Recebido no período",
            variacao_receita["texto"] if variacao_receita else None,
            variacao_receita["cor"] if variacao_receita else "#22C55E"
        )

    with col2:
        card_kpi(
            "Despesas",
            formatar_moeda(total_despesas),
            "📉",
            "#EF553B",
            "Gasto no período",
            variacao_despesa["texto"] if variacao_despesa else None,
            variacao_despesa["cor"] if variacao_despesa else "#EF553B"
        )

    with col3:
        card_kpi(
            "Saldo",
            formatar_moeda(saldo_acumulado),
            "💳",
            "#636EFA",
            "Resultado do período"
        )

    with col4:
        card_kpi(
            "Taxa de Economia",
            f"{taxa_economia_percentual:.1f}%",
            "🚀",
            "#00CC96",
            "Poupado no período"
        )

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        card_kpi(
            "Crescimento Mensal",
            f"{crescimento_patrimonio_percentual:.1f}%",
            "📈",
            "#00CC96",
            "Comparado ao mês anterior"
        )

    with col2:
        card_kpi(
            "Crescimento Anual",
            f"{crescimento_anual:.1f}%",
            "📅",
            "#3B82F6",
            "Comparado aos últimos 12 meses"
        )

    with col3:
        card_kpi(
            "Renda Passiva Anual",
            formatar_moeda(renda_passiva * 12),
            "💵",
            "#00CC96",
            "Receita anual estimada"
        )

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        card_kpi(
            "Meses de Reserva",
            f"{meses_reserva:.1f}",
            "🛡️",
            "#3B82F6",
            "Cobertura das despesas atuais"
        )

    with col2:
        card_kpi(
            "Meta FIRE",
            f"{percentual_independencia:.1f}%",
            "🔥",
            "#8B5CF6",
            "Progresso rumo ao FIRE"
        )

