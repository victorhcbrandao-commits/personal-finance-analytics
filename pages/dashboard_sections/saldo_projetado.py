"""
==============================================================================
FinSight
Módulo: Saldo Mensal Projetado

Responsável pela renderização do gráfico de saldo mensal projetado.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st
import plotly.express as px


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_saldo_projetado(df_resumo_mensal):

    st.subheader("Saldo Mensal Projetado")

    fig = px.bar(
        df_resumo_mensal,
        x="periodo",
        y="Saldo",
        text="Saldo",
        color=df_resumo_mensal["Saldo"].apply(
            lambda x: "Positivo" if x >= 0 else "Negativo"
        ),
        color_discrete_map={
            "Positivo": "#00CC96",
            "Negativo": "#EF553B"
        }
    )

    fig.update_traces(
        texttemplate="R$ %{text:.2f}",
        textposition="outside",
        textfont=dict(
            size=13,
            color="white"
        ),
        marker=dict(
            line=dict(width=0)
        )
    )

    fig.update_xaxes(
        title_text=None,
        showgrid=False
    )

    fig.update_yaxes(
        title_text=None,
        showgrid=True,
        gridcolor="#1f2937",
        zeroline=True,
        zerolinecolor="#94A3B8",
        zerolinewidth=1
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height=420,
        margin=dict(l=20, r=40, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F8FAFC",
            size=12
        ),
        bargap=0.35
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )