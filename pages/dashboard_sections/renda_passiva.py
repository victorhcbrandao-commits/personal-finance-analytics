"""
==============================================================================
FinSight
Módulo: Renda Passiva

Responsável pela renderização da seção de renda passiva e dividendos.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from components.card_kpi import card_kpi
from components.graficos import grafico_dividendos
from src.utils import formatar_moeda


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_renda_passiva(
    renda_passiva,
    df_dividendos_mes,
    df_dividendos_filtrado
):

    st.divider()

    st.header("💵 Renda Passiva")

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

    st.subheader("📈 Dividendos por Mês")

    df_dividendos_filtrado["valor_formatado"] = (
        df_dividendos_filtrado["valor"]
        .apply(formatar_moeda)
    )

    grafico_dividendos(
        df_dividendos_filtrado
    )