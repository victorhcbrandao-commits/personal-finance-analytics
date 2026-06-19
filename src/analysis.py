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

