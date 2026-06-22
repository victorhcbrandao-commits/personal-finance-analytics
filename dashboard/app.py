import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from math import ceil


from io import BytesIO

from src.utils import formatar_moeda
from src.load_data import (
    carregar_transacoes,
    carregar_cartoes,
    carregar_patrimonio,
    carregar_patrimonio_historico,
    carregar_metas,
    carregar_projecao,
    carregar_renda_passiva
)

def card_kpi(titulo, valor, icone, cor):

    st.markdown(
        f"""
<div style='background-color:#111827; padding:20px; border-radius:16px; border:1px solid #1f2937; min-height:120px;'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <span style='font-size:16px; color:#cbd5e1;'>{titulo}</span>
        <span style='font-size:20px;'>{icone}</span>
    </div>
    <div style='font-size:24px; font-weight:700; color:{cor}; margin-top:18px; white-space:nowrap;'>
        {valor}
    </div>
</div>
        """,
        unsafe_allow_html=True
    )

from src.clean_data import limpar_transacoes
from src.cashflow import (
    gerar_fluxo_caixa,
    gerar_resumo_mensal
)
from src.analysis import maiores_despesas
from src.analysis import gastos_por_categoria
from src.analysis import (
    maiores_despesas,
    maiores_receitas,
    gastos_por_categoria,
    despesas_por_cartao,
    proximas_faturas,
    patrimonio_total,
    caixa_total,
    investimentos_total,
    patrimonio_por_instituicao,
    patrimonio_por_tipo,
    calcular_meses_meta,
    renda_passiva_total,
    dividendos_por_mes,
    patrimonio_fire,
    percentual_fire,
    anos_para_fire 
)


st.title(
    "FinSight"
)

st.caption(
    "Panorama completo da sua vida financeira"
)

df = carregar_transacoes("data/raw/transacoes.csv")

df_cartoes = carregar_cartoes("data/raw/cartoes.csv")


df_patrimonio = carregar_patrimonio("data/raw/patrimonio.csv")

patrimonio = patrimonio_total(df_patrimonio)


df_patrimonio_historico = carregar_patrimonio_historico("data/raw/patrimonio_historico.csv")

df_metas = carregar_metas("data/raw/metas.csv")

df_projecao = carregar_projecao("data/raw/projecao.csv")

df_projecao["saldo"] = (
    df_projecao["receita"]
    - df_projecao["despesa"]
)

df_projecao["saldo_acumulado"] = (
    df_projecao["saldo"]
    .cumsum()
)

df_projecao["patrimonio_projetado"] = (
    patrimonio
    + df_projecao["saldo_acumulado"]
)

df_metas["percentual"] = (
    df_metas["atual"]
    / df_metas["objetivo"]
) * 100


df_renda_passiva = carregar_renda_passiva("data/raw/renda_passiva.csv")

renda_passiva = renda_passiva_total(
    df_renda_passiva
)

df_dividendos_mes = dividendos_por_mes(
    df_renda_passiva
)

df = limpar_transacoes(df)

st.sidebar.title(
    "FinSight"
)

pagina = st.sidebar.radio(
    "Menu",
    [
        "🏠 Visão Geral",
        "📈 Fluxo de Caixa",
        "💳 Cartões de Crédito",
        "📅 Planejamento",
        "🎯 Metas",
        "📊 Relatórios",
        "⚙️ Configurações"
    ]
)

st.sidebar.divider()

st.sidebar.subheader(
    "Filtros"
)

meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

meses_invertido = {
    valor: chave
    for chave, valor in meses.items()
}

anos = sorted(df["data_compra"].dt.year.unique())

ano_selecionado = st.sidebar.selectbox(
    "Ano",
    anos
)

df = df[
    df["data_compra"].dt.year == ano_selecionado
]  

meses_disponiveis = sorted(
    df["data_compra"].dt.month.unique()
)

nomes_meses = [
    meses[mes]
    for mes in meses_disponiveis
]

mes_selecionado = st.sidebar.selectbox(
    "Mês",
    ["Todos"] + nomes_meses
)

if mes_selecionado != "Todos":

    numero_mes = meses_invertido[
        mes_selecionado
    ]

    df = df[
        df["data_compra"].dt.month == numero_mes
    ]

categorias = sorted(
    df["categoria"].unique()
)

categoria_selecionada = st.sidebar.selectbox(
    "Categoria",
    ["Todas"] + categorias
)

if categoria_selecionada != "Todas":
    
    df = df[
    df["categoria"] == categoria_selecionada
]

tipo_pagamento_selecionado = st.sidebar.selectbox(
    "Tipo de Pagamento",
    ["Todos"] + sorted(df["tipo_pagamento"].unique())
)
if tipo_pagamento_selecionado != "Todos":

    df = df[
        df["tipo_pagamento"] == tipo_pagamento_selecionado
    ]

top_despesas = maiores_despesas(df)

top_despesas["valor_formatado"] = (
    top_despesas["valor"]
    .apply(
        lambda x:
        f"R$ {x:,.0f}"
        .replace(",", ".")
        if x.is_integer()
        else
        f"R$ {x:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
)

top_receitas = maiores_receitas(df)

top_receitas["valor_formatado"] = (
    top_receitas["valor"]
    .apply(
        lambda x:
        f"R$ {x:,.0f}"
        .replace(",", ".")
        if x.is_integer()
        else
        f"R$ {x:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
)

categorias = gastos_por_categoria(df)

cartoes = despesas_por_cartao(df)

faturas = proximas_faturas(df, df_cartoes)

cartoes["valor_formatado"] = (
    cartoes["valor"]
    .apply(formatar_moeda)
)

df_fluxo_caixa = gerar_fluxo_caixa(df)

df_resumo_mensal = gerar_resumo_mensal(
    df_fluxo_caixa
)

df_resumo_mensal["periodo"] = (
    df_resumo_mensal["ano"].astype(str)
    + "-"
    + df_resumo_mensal["mes"].astype(str).str.zfill(2)
)

total_receitas = df_resumo_mensal["Receita"].sum()

total_despesas = df_resumo_mensal["Despesa"].sum()

saldo_acumulado = df_resumo_mensal["Saldo"].sum()

patrimonio = patrimonio_total(df_patrimonio)

caixa = caixa_total(df_patrimonio)

investimentos = investimentos_total(df_patrimonio)

aporte_mensal = (
    total_receitas
    - total_despesas
)

despesa_anual = (
    total_despesas
    * 12
)

patrimonio_objetivo = patrimonio_fire(
    despesa_anual
)

percentual_independencia = percentual_fire(
    patrimonio,
    patrimonio_objetivo
)

aporte_anual = (
    aporte_mensal
    * 12
)

anos_faltantes = anos_para_fire(
    patrimonio,
    patrimonio_objetivo,
    aporte_anual
)



meses_reserva = calcular_meses_meta(
    50000,
    patrimonio,
    aporte_mensal
)

meses_computador = calcular_meses_meta(
    12000,
    patrimonio,
    aporte_mensal
)

meses_viagem = calcular_meses_meta(
    30000,
    patrimonio,
    aporte_mensal
)

meses_apartamento = calcular_meses_meta(
    150000,
    patrimonio,
    aporte_mensal
)

patrimonio_instituicao = patrimonio_por_instituicao(df_patrimonio)

patrimonio_tipo = patrimonio_por_tipo(df_patrimonio)

st.divider()

st.header(
    "💰 Patrimônio"
)

col1, col2, col3 = st.columns(3)

with col1:
    card_kpi(
        "Patrimônio Total",
        formatar_moeda(patrimonio),
        "💰",
        "#3B82F6"
    )

with col2:
    card_kpi(
        "Caixa",
        formatar_moeda(caixa),
        "💵",
        "#00CC96"
    )

with col3:
    card_kpi(
        "Investimentos",
        formatar_moeda(investimentos),
        "📈",
        "#F59E0B"
    )


st.subheader(
    "Patrimônio por Instituição"
)

patrimonio_instituicao["valor_formatado"] = (
    patrimonio_instituicao["valor"]
    .apply(formatar_moeda)
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
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Patrimônio por Tipo"
)

patrimonio_tipo["valor_formatado"] = (
    patrimonio_tipo["valor"]
    .apply(formatar_moeda)
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
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    },
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader(
    "Evolução Patrimonial"
)

fig = px.line(
    df_patrimonio_historico,
    x="data",
    y="patrimonio",
    markers=True
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

quantidade_transacoes= len(df)


col1, col2, col3, col4 = st.columns(4)

with col1:
    card_kpi("Receitas", formatar_moeda(total_receitas), "💰", "#00CC96")

with col2:
    card_kpi("Despesas", formatar_moeda(total_despesas), "📉", "#EF553B")

with col3:
    card_kpi("Saldo", formatar_moeda(saldo_acumulado), "💳", "#636EFA")

with col4:
    card_kpi("Transações", quantidade_transacoes, "📊", "#FFFFFF")

st.subheader(
    "Saldo Mensal Projetado"
)

fig = px.line(
    df_resumo_mensal,
    x="periodo",
    y="Saldo",
    markers=True
)

fig.update_layout(
    xaxis_title="Período",
    yaxis_title="Valor",
    legend_title="Tipo"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

df_grafico = df_resumo_mensal.copy()

df_grafico["Saldo Acumulado"] = (
    df_grafico["Saldo"].cumsum()
)


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
            color="#636EFA",
            width=3
        ),
        marker=dict(size=8)
    )
)

fig.update_layout(

    barmode="group",

    xaxis_title="",

    yaxis_title="",

    template="plotly_dark",

    height=500,

    hovermode="x unified",

    legend=dict(
        orientation="h",
        x=0,
        y=1.10
    )
)

st.subheader(
    "Fluxo de Caixa Mensal"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Top Maiores Despesas"
)


fig = px.bar(
    top_despesas,
    x="valor",
    y="descricao",
    orientation="h",
    text="valor"
)

fig.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    }
)

fig.update_traces(
    text=top_despesas["valor_formatado"],
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Valor (R$)",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    }
)

fig.update_xaxes(
    range=[0, top_despesas["valor"].max() * 1.25]
)

fig.update_xaxes(
    visible=False
)

fig.update_layout(
    xaxis_title="Valor (R$)",
    yaxis_title="",
    showlegend=False
)

fig.update_layout(
    xaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Top Receitas"
)

fig = px.bar(
    top_receitas,
    x="valor",
    y="descricao",
    orientation="h",
    text="valor_formatado",
    color_discrete_sequence=["#00CC96"]
)

fig.update_traces(
    textposition="outside"
)

fig.update_xaxes(
    range=[0, top_receitas["valor"].max() * 1.25],
    visible=False
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Gastos por Categoria"
)

st.dataframe(
    categorias,
    hide_index=True
)

fig = px.bar(
    categorias,
    x="categoria",
    y="valor",
    text="valor"
)

fig.update_layout(
    xaxis_title="Categoria",
    yaxis_title="Valor",
    showlegend=False
)

fig.update_traces(
    texttemplate="R$ %{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Despesas por Cartão"
)

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


fig.update_layout(
    showlegend=False
)

fig.update_traces(
    texttemplate="%{text}",
    textposition="outside"
)

fig.update_xaxes(
    range=[0, cartoes["valor"].max() * 1.35],
    visible=False
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    showlegend=False,
    yaxis={
        "categoryorder": "total ascending"
    },
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Distribuição dos Gastos"
)

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
    hole=0.65
)

fig.update_traces(
    text=df_pizza["texto"],
    textinfo="text",
    textposition="inside"
)

fig.update_layout(
    showlegend=True,

    legend=dict(
        x=0.83,
        y=0.95
    ),

    margin=dict(
        t=20,
        b=20,
        l=20,
        r=20
    ),

    annotations=[
        dict(
            text=f"{valor_total}<br>Despesas",
            x=0.5,
            y=0.5,
            font_size=22,
            showarrow=False
        )
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

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

excel = df_exibicao.to_excel(
    "transacoes.xlsx",
    index=False
)

st.subheader(
    "Transações"
)

st.dataframe(
    df_exibicao
)

st.divider()

st.header(
    "💳 Cartões"
)

st.subheader(
    "Próximas Faturas"
)

col1, col2, col3 = st.columns(3)

for i, (_, linha) in enumerate(faturas.iterrows()):

    coluna = [col1, col2, col3][i % 3]

    valor_fatura = linha["valor"]

    limite_total = linha["limite"]

    limite_disponivel = limite_total - valor_fatura

    percentual_utilizado = (
        valor_fatura / limite_total
    ) * 100

    largura_barra = max(
    percentual_utilizado,
    3
)
    
    cores_cartoes = {
    "Black Visa": "#F59E0B",
    "Black Master": "#EF4444",
    "Azul Platinum": "#2563EB"
}

    cor_cartao = cores_cartoes.get(
    linha["cartao"],
    "#3B82F6"
)

    with coluna:

        st.markdown(
    f"""
<div style='background-color:#111827; border:1px solid #1f2937; border-radius:16px; padding:20px; min-height:290px;'>
    <div style='font-size:20px; font-weight:700; color:white;'>💳 {linha["apelido"]}</div>
    <div style='color:#9ca3af; margin-top:8px;'>🏦 {linha["banco"]}</div>
    <div style='font-size:28px; font-weight:700; color:white; margin-top:20px; white-space:nowrap;'>{formatar_moeda(linha["valor"])}</div>
    <div style='color:#9ca3af; margin-top:18px;'>{percentual_utilizado:.1f}% utilizado</div>
    <div style='width:100%; height:10px; background-color:#1f2937; border-radius:8px; margin-top:10px;'><div style='width:{largura_barra}%; height:10px; background-color:{cor_cartao}; border-radius:8px;'></div></div>
    <div style='color:#9ca3af; margin-top:18px;'>Limite disponível</div>
    <div style='font-size:18px; color:#00CC96; font-weight:700;'>{formatar_moeda(limite_disponivel)}</div>
    <div style='color:#9ca3af; margin-top:20px;'>📅 Vencimento: dia {linha["vencimento"]}</div>
    <div style='color:#9ca3af; margin-top:8px;'>💳 {linha["bandeira"]}</div>
</div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.header(
    "🎯 Planejamento"
)

patrimonio_dezembro = (
    df_projecao["patrimonio_projetado"]
    .iloc[-1]
)

col1, col2 = st.columns(2)

with col1:

    card_kpi(
        "Patrimônio Projetado",
        formatar_moeda(
            patrimonio_dezembro
        ),
        "🚀",
        "#3B82F6"
    )

with col2:

    crescimento = (patrimonio_dezembro - patrimonio)

    card_kpi(
        "Crescimento Projetado",
        formatar_moeda(
            crescimento
        ),
        "📈",
        "#00CC96"
    )
        

st.subheader(
    "Metas Financeiras"
)

col1, col2 = st.columns(2)


for i, (_, linha) in enumerate(df_metas.iterrows()):

    meses_para_meta = calcular_meses_meta(
    linha["objetivo"],
    patrimonio,
    aporte_mensal
)

    meses_para_meta = ceil(
        meses_para_meta
)

    if meses_para_meta == 0:
        previsao_meta = "✅ Já atingida"
    else:
        previsao_meta = f"📅 Faltam {meses_para_meta} meses"

    coluna = [col1, col2][i % 2]

    largura_barra = max(
        linha["percentual"],
        3
    )

    with coluna:

        st.markdown(
            f"""
<div style='background-color:#111827; border:1px solid #1f2937; border-radius:16px; padding:20px; min-height:220px;'>

<div style='font-size:22px; font-weight:700; color:white;'>
🎯 {linha["meta"]}
</div>

<div style='color:#9ca3af; margin-top:15px;'>
{formatar_moeda(linha["atual"])} / {formatar_moeda(linha["objetivo"])}
</div>

<div style='font-size:28px; font-weight:700; color:{linha["cor"]}; margin-top:20px;'>
{linha["percentual"]:.1f}%
</div>

<div style='width:100%; height:10px; background-color:#1f2937; border-radius:8px; margin-top:15px;'><div style='width:{largura_barra}%; height:10px; background-color:{linha["cor"]}; border-radius:8px;'></div></div>

<div style='color:#9ca3af; margin-top:18px;'>{previsao_meta}</div>

</div>
            """,
            unsafe_allow_html=True
        )
        
st.divider()

st.header(
    "📈 Projeções"
)

st.subheader(
    "Projeção Financeira"
)

fig = px.line(
    df_projecao,
    x="mes",
    y="patrimonio_projetado",
    markers=True
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.header(
    "💵 Renda Passiva"
)

col1, col2 = st.columns(2)

with col1:
    card_kpi(
        "Renda Passiva Total",
        formatar_moeda(renda_passiva),
        "💵",
        "#00CC96"
    )

with col2:
    media_mensal = df_dividendos_mes["valor"].mean()

    card_kpi(
        "Média Mensal",
        formatar_moeda(media_mensal),
        "📈",
        "#3B82F6"
    )

    st.subheader(
    "Dividendos por Mês"
)

df_dividendos_mes["valor_formatado"] = (
    df_dividendos_mes["valor"]
    .apply(formatar_moeda)
)

fig = px.bar(
    df_dividendos_mes,
    x="mes",
    y="valor",
    text="valor_formatado"
)

fig.update_traces(
    texttemplate="%{text}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    template="plotly_dark",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.header(
    "🔥 Independência Financeira"
)

col1, col2, col3 = st.columns(3)

with col1:

    card_kpi(
        "Patrimônio FIRE",
        formatar_moeda(
            patrimonio_objetivo
        ),
        "🔥",
        "#EF4444"
    )

with col2:

    card_kpi(
        "Progresso FIRE",
        f"{percentual_independencia:.1f}%",
        "📈",
        "#F59E0B"
    )

with col3:

    card_kpi(
        "Anos Restantes",
        f"{anos_faltantes:.1f}",
        "📅",
        "#8B5CF6"
    )

largura_fire = max(
    percentual_independencia,
    3
)

st.subheader(
    "Progresso para Independência Financeira"
)

st.markdown(
    f"""
<div style='width:100%; height:16px; background-color:#1f2937; border-radius:8px;'>

<div style='width:{largura_fire}%; height:16px; background-color:#EF4444; border-radius:8px;'>
</div>

</div>

<div style='margin-top:12px; color:#9ca3af;'>
{percentual_independencia:.2f}% concluído
</div>
""",
    unsafe_allow_html=True
)