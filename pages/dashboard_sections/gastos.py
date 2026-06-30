"""
==============================================================================
FinSight
Módulo: Gastos e Despesas

Responsável pela renderização das análises de despesas, receitas, categorias,
cartões e distribuição dos gastos.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import streamlit as st
import plotly.express as px

from src.utils import formatar_moeda


# ==============================================================================
# RENDERIZAÇÃO
# ==============================================================================

def renderizar_gastos(
    top_despesas,
    top_receitas,
    categorias,
    cartoes
):

    # ==========================================================================
    # TOP MAIORES DESPESAS
    # ==========================================================================

    st.subheader("Top Maiores Despesas")

    fig = px.bar(
        top_despesas,
        x="valor",
        y="descricao",
        orientation="h",
        text="valor_formatado",
        color_discrete_sequence=["#EF553B"]
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont=dict(size=13, color="white"),
        marker=dict(color="#EF553B", line=dict(width=0))
    )

    fig.update_xaxes(
        range=[0, top_despesas["valor"].max() * 1.45],
        visible=False,
        showgrid=False
    )

    fig.update_yaxes(title="", showgrid=False)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        yaxis={"categoryorder": "total ascending"},
        height=420,
        margin=dict(l=20, r=100, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", size=12),
        bargap=0.25
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

    # ==========================================================================
    # TOP RECEITAS
    # ==========================================================================

    st.subheader("Top Receitas")

    fig = px.bar(
        top_receitas,
        x="valor",
        y="descricao",
        orientation="h",
        text="valor_formatado",
        color_discrete_sequence=["#00CC96"]
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont=dict(size=13, color="white"),
        marker=dict(color="#00CC96", line=dict(width=0))
    )

    fig.update_xaxes(
        range=[0, top_receitas["valor"].max() * 1.35],
        visible=False,
        showgrid=False
    )

    fig.update_yaxes(title="", showgrid=False)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        yaxis={"categoryorder": "total ascending"},
        height=280,
        margin=dict(l=20, r=100, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", size=12),
        bargap=0.25
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

    # ==========================================================================
    # GASTOS POR CATEGORIA
    # ==========================================================================

    st.subheader("Gastos por Categoria")

    categorias_exibir = categorias.copy()

    categorias_exibir["valor"] = (
        categorias_exibir["valor"]
        .apply(formatar_moeda)
    )

    categorias_exibir = categorias_exibir.rename(
        columns={
            "categoria": "Categoria",
            "valor": "Valor"
        }
    )

    st.dataframe(
        categorias_exibir,
        hide_index=True,
        width="stretch"
    )

    fig = px.bar(
        categorias,
        x="categoria",
        y="valor",
        text="valor",
        color_discrete_sequence=["#EF553B"]
    )

    fig.update_traces(
        texttemplate="R$ %{text:.2f}",
        textposition="outside",
        textfont=dict(size=13, color="white"),
        marker=dict(color="#EF553B", line=dict(width=0))
    )

    fig.update_yaxes(
        title="",
        showgrid=True,
        gridcolor="#1f2937"
    )

    fig.update_xaxes(
        title="",
        showgrid=False
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=420,
        margin=dict(l=20, r=40, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", size=12),
        bargap=0.35
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

    # ==========================================================================
    # DESPESAS POR CARTÃO
    # ==========================================================================

    st.subheader("Despesas por Cartão")

    fig = px.bar(
        cartoes,
        x="valor",
        y="cartao",
        orientation="h",
        text="valor_formatado",
        color="cartao",
        color_discrete_map={
            "Black Visa": "#F59E0B",
            "Black Master": "#EF4444",
            "Azul Platinum": "#2563EB"
        }
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont=dict(size=13, color="white"),
        marker=dict(line=dict(width=0))
    )

    fig.update_xaxes(
        range=[0, cartoes["valor"].max() * 1.45],
        visible=False,
        showgrid=False
    )

    fig.update_yaxes(title="", showgrid=False)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        yaxis={"categoryorder": "total ascending"},
        height=420,
        margin=dict(l=20, r=100, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", size=12),
        bargap=0.25
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

    # ==========================================================================
    # DISTRIBUIÇÃO DOS GASTOS
    # ==========================================================================

    st.subheader("Distribuição dos Gastos")

    df_pizza = categorias.reset_index()

    df_pizza["percentual"] = (
        df_pizza["valor"]
        / df_pizza["valor"].sum()
        * 100
    )

    df_pizza["texto"] = df_pizza["percentual"].apply(
        lambda x: f"{x:.1f}%" if x >= 5 else ""
    )

    valor_total = (
        f"R$ {df_pizza['valor'].sum():,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    fig = px.pie(
        df_pizza,
        names="categoria",
        values="valor",
        hole=0.72,
        color_discrete_sequence=[
            "#3B82F6",
            "#00CC96",
            "#F59E0B",
            "#EF553B",
            "#8B5CF6",
            "#EC4899"
        ]
    )

    fig.update_traces(
        text=df_pizza["texto"],
        textinfo="text",
        textposition="inside",
        textfont=dict(size=14, color="white"),
        marker=dict(
            line=dict(
                color="#111827",
                width=2
            )
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", size=12),
        showlegend=True,
        legend=dict(x=1.02, y=0.95),
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[
            dict(
                text=f"<b>{valor_total}</b><br>Despesas",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=24, color="white")
            )
        ]
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )