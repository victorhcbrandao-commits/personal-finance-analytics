"""
==============================================================================
FinSight
Módulo: Fluxo de Caixa

Responsável pela renderização do gráfico de fluxo de caixa mensal.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_fluxo_caixa(df_resumo_mensal):

    # ==========================================================================
    # PREPARAÇÃO DOS DADOS
    # ==========================================================================

    df_grafico = df_resumo_mensal.copy()

    df_grafico["Saldo Acumulado"] = (
        df_grafico["Saldo"].cumsum()
    )

    # ==========================================================================
    # GRÁFICO
    # ==========================================================================

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

    # ==========================================================================
    # EXIBIÇÃO
    # ==========================================================================

    st.subheader("Fluxo de Caixa Mensal")

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )