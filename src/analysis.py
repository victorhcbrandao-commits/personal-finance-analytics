def calcular_receitas(df):
            
    receitas = df[df["tipo_pagamento"] == "Receita"]["valor"].sum()

    return receitas


def calcular_despesas(df):
            
    despesas = df[df["tipo_pagamento"] != "Receita"]["valor"].sum()

    return despesas


def calcular_saldo(df):

    receitas = calcular_receitas(df)

    despesas = calcular_despesas(df)

    saldo = receitas - despesas

    return saldo


def gastos_por_categoria(df):

    despesas = df[df["tipo_pagamento"] != "Receita"]

    categorias = despesas.groupby("categoria")["valor"].sum()

    categorias = categorias.sort_values(
        ascending=False
    )

    return categorias.reset_index()


def maiores_despesas(df, quantidade=5):

    despesas = df[df["tipo_pagamento"] != "Receita"]

    maiores_despesas = despesas.groupby(
        "descricao"
        )["valor"].sum() 

    maiores_despesas = maiores_despesas.sort_values(
        ascending=False
        )
    
    maiores_despesas = maiores_despesas.head(
        quantidade
    )    

    return maiores_despesas.reset_index()

def maiores_receitas(df, quantidade=5):

    receitas = df[
        df["tipo_pagamento"] == "Receita"
    ]

    maiores_receitas = receitas.groupby(
        "descricao"
    )["valor"].sum()

    maiores_receitas = maiores_receitas.sort_values(
        ascending=False
    )

    maiores_receitas = maiores_receitas.head(
        quantidade
    )

    return maiores_receitas.reset_index()


def despesas_por_cartao(df):

    despesas_cartao = df[
        df["tipo_pagamento"] == "Cartão"
    ]

    cartoes = despesas_cartao.groupby(
        "cartao"
    )["valor"].sum()

    cartoes = cartoes.sort_values(
        ascending=False
    )

    return cartoes.reset_index()


def proximas_faturas(
        df_transacoes,
        df_cartoes):

    despesas_cartao = df_transacoes[
        df_transacoes["tipo_pagamento"] == "Cartão"
    ]

    faturas = despesas_cartao.groupby(
        "cartao"
    )["valor"].sum()

    faturas = faturas.reset_index()

    faturas = faturas.merge(
        df_cartoes,
        on="cartao",
        how="left"
    )

    return faturas


def patrimonio_total(df):

    return df["valor"].sum()


def caixa_total(df):

    caixa = df[
        df["tipo"] == "Conta Corrente"
    ]

    return caixa["valor"].sum()


def investimentos_total(df):

    investimentos = df[
        df["tipo"] != "Conta Corrente"
    ]

    return investimentos["valor"].sum()


def patrimonio_por_instituicao(df):

    patrimonio = df.groupby(
        "instituicao"
    )["valor"].sum()

    patrimonio = patrimonio.sort_values(
        ascending=False
    )

    return patrimonio.reset_index()

def patrimonio_por_instituicao(df):

    patrimonio = df.groupby(
        "instituicao"
    )["valor"].sum()

    patrimonio = patrimonio.sort_values(
        ascending=False
    )

    return patrimonio.reset_index()

def patrimonio_por_tipo(df):

    patrimonio = df.groupby(
        "tipo"
    )["valor"].sum()

    patrimonio = patrimonio.sort_values(
        ascending=False
    )

    return patrimonio.reset_index()


def calcular_meses_meta(objetivo, patrimonio_atual, aporte_mensal):

    if patrimonio_atual >= objetivo:
        return 0

    meses = (
        objetivo
        - patrimonio_atual
    ) / aporte_mensal

    return meses


def renda_passiva_total(df):

    return df["valor"].sum()



def dividendos_por_mes(df):

    df = df.copy()

    df["mes"] = df["data"].dt.strftime(
        "%b/%y"
    )

    renda = (
        df.groupby(
            "mes"
        )["valor"]
        .sum()
        .reset_index()
    )

    return renda

def patrimonio_fire(despesa_anual):

    return despesa_anual / 0.04

def percentual_fire(
    patrimonio_atual,
    patrimonio_objetivo
):

    return (
        patrimonio_atual
        / patrimonio_objetivo
    ) * 100

def anos_para_fire(
    patrimonio_atual,
    patrimonio_objetivo,
    aporte_anual
):

    faltante = (
        patrimonio_objetivo
        - patrimonio_atual
    )

    if faltante <= 0:
        return 0

    anos = (
        faltante
        / aporte_anual
    )

    return anos

