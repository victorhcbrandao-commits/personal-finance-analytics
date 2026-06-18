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
