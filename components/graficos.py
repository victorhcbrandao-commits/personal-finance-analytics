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
        use_container_width=True
    )