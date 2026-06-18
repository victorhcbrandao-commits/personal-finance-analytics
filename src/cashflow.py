import pandas as pd

from src.cards import gerar_parcelas

def gerar_fluxo_caixa(df):

    lista_fluxo_caixa = []

    for indice, linha in df.iterrows():

        if linha["tipo_pagamento"] == "Cartão":

            print(
                linha["descricao"],
                linha["tipo_pagamento"],
                linha["cartao"]
            )

        
            parcelas = gerar_parcelas(
                linha["descricao"],
                linha["valor"],
                linha["parcelas"],
                linha["data_compra"],
                linha["cartao"]
        )

            lista_fluxo_caixa.extend(parcelas)

    df_fluxo_caixa = pd.DataFrame(
        lista_fluxo_caixa
        )

    return df_fluxo_caixa