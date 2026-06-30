"""
==============================================================================
FinSight
Módulo: Patrimônio

Responsável pela renderização completa da seção de patrimônio do dashboard.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from components.card_kpi import card_kpi
from components.graficos import (
    grafico_patrimonio_instituicao,
    grafico_patrimonio_tipo,
    grafico_evolucao_patrimonial
)
from src.utils import formatar_moeda


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_patrimonio(
    patrimonio,
    caixa,
    investimentos,
    patrimonio_instituicao,
    patrimonio_tipo,
    df_historico_filtrado
):
    
    st.header("💰 Patrimônio")

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

    st.subheader("Patrimônio por Instituição")

    patrimonio_instituicao["valor_formatado"] = (
        patrimonio_instituicao["valor"]
        .apply(formatar_moeda)
    )

    grafico_patrimonio_instituicao(
        patrimonio_instituicao
    )

    st.subheader("Patrimônio por Tipo")

    patrimonio_tipo["valor_formatado"] = (
        patrimonio_tipo["valor"]
        .apply(formatar_moeda)
    )

    grafico_patrimonio_tipo(
        patrimonio_tipo
    )

    st.subheader("Evolução Patrimonial")

    grafico_evolucao_patrimonial(
        df_historico_filtrado
    )