import streamlit as st
import plotly.express as px


def grafico_patrimonio_instituicao(patrimonio_instituicao):

    patrimonio_instituicao = patrimonio_instituicao.copy()

    fig = px.bar(
        patrimonio_instituicao,
        x="valor",
        y="instituicao",
        orientation="h",
        text="valor_formatado",
        color_discrete_sequence=["#3B82F6"]
    )

    fig.update_traces(
    texttemplate="%{text}",
    textposition="outside",
    textfont=dict(
        size=13,
        color="white"
    ),
    marker=dict(
        color="#3B82F6",
        line=dict(width=0)
    )
)

    fig.update_xaxes(
        range=[0, patrimonio_instituicao["valor"].max() * 1.15],
        visible=False,
        showgrid=False
    )

    fig.update_yaxes(
        title="",
        showgrid=False
    )

    fig.update_layout(
        bargap=0.25,
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=100, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F8FAFC",
            size=12
        ),
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )


def grafico_patrimonio_tipo(patrimonio_tipo):

    patrimonio_tipo = patrimonio_tipo.copy()

    fig = px.bar(
        patrimonio_tipo,
        x="valor",
        y="tipo",
        orientation="h",
        text="valor_formatado",
        color_discrete_sequence=["#3B82F6"]
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont=dict(
            size=13,
            color="white"
        ),
        marker=dict(
            color="#3B82F6",
            line=dict(width=0)
        )
    )

    fig.update_xaxes(
        range=[0, patrimonio_tipo["valor"].max() * 1.35],
        visible=False,
        showgrid=False
    )

    fig.update_yaxes(
        title="",
        showgrid=False
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        yaxis={
            "categoryorder": "total ascending"
        },
        height=450,
        margin=dict(l=20, r=100, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F8FAFC",
            size=12
        ),
        bargap=0.25
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )


def grafico_evolucao_patrimonial(df_patrimonio_historico):

    fig = px.area(
        df_patrimonio_historico,
        x="data",
        y="patrimonio"
    )

    fig.update_traces(
        line=dict(
            color="#3B82F6",
            width=4
        ),
        marker=dict(
            size=8,
            color="#93C5FD",
            line=dict(
                width=2,
                color="#3B82F6"
            )
        ),
        fillcolor="rgba(59,130,246,0.15)"
    )

    fig.update_xaxes(
        title_text=None,
        showgrid=False
    )

    fig.update_yaxes(
    title_text=None,
    showgrid=True,
    gridcolor="#1f2937",
    range=[
        df_patrimonio_historico["patrimonio"].min() * 0.95,
        df_patrimonio_historico["patrimonio"].max() * 1.05
    ]
)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F8FAFC",
            size=12
        )
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

def grafico_projecao(df_projecao):

    fig = px.area(
        df_projecao,
        x="mes",
        y="patrimonio_projetado"
    )

    fig.update_traces(
        line=dict(
            color="#3B82F6",
            width=4
        ),
        fillcolor="rgba(59,130,246,0.15)"
    )

    fig.update_xaxes(
        title_text=None,
        showgrid=False
    )

    fig.update_yaxes(
        title_text=None,
        showgrid=True,
        gridcolor="#1f2937",
        range=[
            df_projecao["patrimonio_projetado"].min() * 0.95,
            df_projecao["patrimonio_projetado"].max() * 1.05
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F8FAFC",
            size=12
        )
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

def grafico_dividendos(dividendos_mes):

    fig = px.bar(
        dividendos_mes,
        x="mes",
        y="valor",
        text="valor_formatado",
        color_discrete_sequence=["#22C55E"]
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont=dict(
            size=13,
            color="white"
        ),
        marker=dict(
            color="#22C55E",
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
        gridcolor="#1f2937"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height=420,
        margin=dict(
            l=20,
            r=40,
            t=40,
            b=20
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F8FAFC",
            size=12
        ),
        bargap=0.25
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )