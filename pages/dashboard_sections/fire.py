"""
==============================================================================
FinSight
Módulo: Independência Financeira (FIRE)

Responsável pela renderização da seção de independência financeira.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from components.card_fire import card_fire


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_fire(
    patrimonio_objetivo,
    percentual_independencia,
    anos_faltantes,
    formatar_moeda
):

    st.divider()

    st.header("🔥 Independência Financeira")

    col1, col2, col3 = st.columns(3)

    card_fire(
        patrimonio_objetivo,
        percentual_independencia,
        anos_faltantes,
        formatar_moeda
    )