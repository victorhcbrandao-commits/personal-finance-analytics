import pandas as pd

from src.cards import gerar_parcelas

def gerar_fluxo_caixa(df):

    lista_fluxo_caixa = []

    for indice, linha in df.iterrows():

        if linha["tipo_pagamento"] == "Cartão":

               
            parcelas = gerar_parcelas(
                linha["descricao"],
                linha["valor"],
                linha["parcelas"],
                linha["data_compra"],
                linha["cartao"]
        )

            lista_fluxo_caixa.extend(parcelas)

        else:

            transacao = {
                "descricao": linha["descricao"],
                "parcela": "1/1",
                "valor": linha["valor"],
                "data_fatura": linha["data_compra"],
                "origem_pagamento": linha["tipo_pagamento"]
            }

            lista_fluxo_caixa.append(transacao)

    df_fluxo_caixa = pd.DataFrame(
        lista_fluxo_caixa
        )

    return df_fluxo_caixa

def gerar_resumo_mensal(df_fluxo_caixa):

    df_fluxo_caixa["ano"] = df_fluxo_caixa["data_fatura"].dt.year

    df_fluxo_caixa["mes"] = df_fluxo_caixa["data_fatura"].dt.month

    df_fluxo_caixa["tipo_fluxo"] = df_fluxo_caixa["origem_pagamento"].apply(
        lambda origem: "Receita" if origem == "Receita" else "Despesa"
    )

    resumo = df_fluxo_caixa.groupby(
        ["ano", "mes", "tipo_fluxo"]
    )["valor"].sum()

    resumo = resumo.reset_index()

    resumo = resumo.pivot_table(
        index=["ano", "mes"],
        columns="tipo_fluxo",
        values="valor",
        fill_value=0 
    )

    resumo["Saldo"] = resumo["Receita"] - resumo["Despesa"]

    return resumo