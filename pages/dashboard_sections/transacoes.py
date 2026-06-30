"""
==============================================================================
FinSight
Módulo: Transações e Exportação

Responsável pela renderização da tabela de transações e exportação em Excel.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st

from io import BytesIO


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_transacoes(df):

    # ==========================================================================
    # PREPARAÇÃO DOS DADOS
    # ==========================================================================

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

    # ==========================================================================
    # EXPORTAÇÃO EXCEL
    # ==========================================================================

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

    # ==========================================================================
    # TABELA
    # ==========================================================================

    st.subheader("Transações")

    st.dataframe(
        df_exibicao,
        width="stretch"
    )