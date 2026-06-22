import pandas as pd


def carregar_transacoes(caminho):
    
    df = pd.read_csv(caminho)

    df["data_compra"] = pd.to_datetime(
        df["data_compra"],
        dayfirst=True
    )

    return df

def carregar_cartoes(caminho):

    return pd.read_csv(
        caminho
    )
