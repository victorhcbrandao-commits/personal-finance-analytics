import streamlit as st
import plotly.express as px


def grafico_patrimonio_instituicao(
    patrimonio_instituicao
):

    patrimonio_instituicao = (
        patrimonio_instituicao.copy()
    )

    fig = px.bar(
        patrimonio_instituicao,
        x="valor",
        y="instituicao",
        orientation="h",
        text="valor_formatado"
    )

    fig.update_traces(
    texttemplate="%{text}",
    textposition="outside"
)

    fig.update_xaxes(
    range=[
        0,
        patrimonio_instituicao["valor"].max() * 1.25
    ],
    visible=False
)

    fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    },
    template="plotly_dark",
    height=420
)

    st.plotly_chart(
    fig,
    width="stretch"
)


def grafico_patrimonio_tipo(
    patrimonio_tipo
):

    patrimonio_tipo = (
        patrimonio_tipo.copy()
    )

    fig = px.bar(
        patrimonio_tipo,
        x="valor",
        y="tipo",
        orientation="h",
        text="valor_formatado"
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )

    fig.update_xaxes(
        range=[
            0,
            patrimonio_tipo["valor"].max() * 1.25
        ],
        visible=False
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        yaxis={
            "categoryorder": "total ascending"
        },
        height=420
    )

    st.plotly_chart(
    fig,
    width="stretch"
)


def grafico_evolucao_patrimonial(
    df_patrimonio_historico
):

    fig = px.line(
        df_patrimonio_historico,
        x="data",
        y="patrimonio",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=450
    )

    st.plotly_chart(
    fig,
    width="stretch"
)

def grafico_projecao(
    df_projecao
):

    fig = px.line(
        df_projecao,
        x="mes",
        y="patrimonio_projetado",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=450
    )

    st.plotly_chart(
    fig,
    width="stretch"
)

def grafico_dividendos(
    dividendos_mes
):

    fig = px.bar(
        dividendos_mes,
        x="mes",
        y="valor",
        text="valor_formatado"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=450
    )

    st.plotly_chart(
    fig,
    width="stretch"
)