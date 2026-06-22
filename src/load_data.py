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

def carregar_patrimonio(caminho):

    return pd.read_csv(
        caminho
    )

def carregar_patrimonio_historico(caminho):

    df = pd.read_csv(
        caminho
    )

    df["data"] = pd.to_datetime(
        df["data"],
        dayfirst=True
    )

    return df

def carregar_metas(caminho):

    return pd.read_csv(
        caminho
    )

def carregar_projecao(caminho):

    return pd.read_csv(
        caminho
    )

def carregar_renda_passiva(caminho):

    df = pd.read_csv(
        caminho
    )

    df["data"] = pd.to_datetime(
        df["data"],
        dayfirst=True
    )

    return df