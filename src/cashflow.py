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