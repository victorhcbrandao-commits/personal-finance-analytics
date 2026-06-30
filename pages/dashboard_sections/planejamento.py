"""
==============================================================================
FinSight
Módulo: Planejamento

Responsável pela renderização da seção de planejamento e metas financeiras.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from components.card_kpi import card_kpi
from components.card_meta import card_meta
from src.utils import formatar_moeda


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_planejamento(
    df_projecao,
    df_metas,
    patrimonio,
    aporte_mensal,
    calcular_meses_meta
):

    st.divider()

    st.header("🎯 Planejamento")

    patrimonio_dezembro = (
        df_projecao["patrimonio_projetado"]
        .iloc[-1]
    )

    col1, col2 = st.columns(2)

    with col1:
        card_kpi(
            "Patrimônio Projetado",
            formatar_moeda(patrimonio_dezembro),
            "🚀",
            "#3B82F6"
        )

    with col2:
        crescimento = patrimonio_dezembro - patrimonio

        card_kpi(
            "Crescimento Projetado",
            formatar_moeda(crescimento),
            "📈",
            "#00CC96"
        )

    st.subheader("Metas Financeiras")

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