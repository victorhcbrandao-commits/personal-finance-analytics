"""
==============================================================================
FinSight
Módulo: Cartões

Responsável pela renderização da seção de cartões de crédito e próximas faturas.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from components.card_cartao import card_cartao


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_cartoes(
    faturas_filtrado,
    formatar_moeda
):

    st.divider()

    st.header("💳 Cartões")

    st.subheader("Próximas Faturas")

    col1, col2, col3 = st.columns(3)

    for i, (_, linha) in enumerate(faturas_filtrado.iterrows()):

        coluna = [col1, col2, col3][i % 3]

        with coluna:
            card_cartao(
                linha,
                formatar_moeda
            )