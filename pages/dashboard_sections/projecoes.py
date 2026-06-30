"""
==============================================================================
FinSight
Módulo: Projeções

Responsável pela renderização da seção de projeções financeiras.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from components.graficos import grafico_projecao


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_projecoes(df_projecao):

    st.divider()

    st.header("📈 Projeções")

    st.subheader("Projeção Financeira")

    grafico_projecao(
        df_projecao
    )