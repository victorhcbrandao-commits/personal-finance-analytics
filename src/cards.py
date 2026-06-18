from dateutil.relativedelta import relativedelta
from datetime import datetime   

cartoes = {
    "Azul Platinum": {
        "fechamento": 25,
        "vencimento": 1
    },
    "Black Master": {
        "fechamento": 29,
        "vencimento": 5
    },
    "Black Visa": {
        "fechamento": 29,
        "vencimento": 5
    }
}

def obter_dia_fechamento(cartao):

    dia_fechamento = cartoes[cartao]["fechamento"]

    return dia_fechamento


def obter_dia_vencimento(cartao):

    dia_vencimento = cartoes[cartao]["vencimento"]

    return dia_vencimento   


def calcular_fatura(data_compra, cartao):

    dia_compra = data_compra.day

    dia_fechamento = obter_dia_fechamento(cartao)

    dia_vencimento = obter_dia_vencimento(cartao)

    if dia_compra <= dia_fechamento:
        data_fatura = data_compra + relativedelta(months=1)
    else:
        data_fatura = data_compra + relativedelta(months=2)

    data_vencimento = datetime(
        data_fatura.year,
        data_fatura.month,
        dia_vencimento
    )

    return data_vencimento


def gerar_parcelas(descricao, valor, parcelas, data_compra, cartao):

    valor_parcela = valor / parcelas

    lista_parcelas = []

    primeira_fatura = calcular_fatura(
        data_compra,
        cartao
    )

    for numero_parcela in range(1, parcelas + 1):

        data_parcela = primeira_fatura + relativedelta(
            months=numero_parcela - 1
        )

        parcela = {
            "descricao": descricao,
            "parcela": f"{numero_parcela}/{parcelas}",
            "valor": valor_parcela,
            "data_fatura": data_parcela,
            "origem_pagamento": cartao
        }

        lista_parcelas.append(parcela)

    return lista_parcelas