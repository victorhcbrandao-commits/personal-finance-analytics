from src.utils import calcular_variacao_percentual


def calcular_variacao_receita(receita_atual, receita_anterior):
    """
    Calcula a variação percentual das receitas.
    """
    return calcular_variacao_percentual(
        receita_atual,
        receita_anterior
    )


def calcular_variacao_despesa(despesa_atual, despesa_anterior):
    """
    Calcula a variação das despesas.

    Para despesas:
    ↑ aumento = ruim
    ↓ redução = bom
    """

    variacao = calcular_variacao_percentual(
        despesa_atual,
        despesa_anterior
    )

    if variacao is None:
        return None

    if variacao["tipo"] == "positivo":
        variacao["cor"] = "#EF553B"

    elif variacao["tipo"] == "negativo":
        variacao["cor"] = "#22C55E"

    return variacao


def calcular_variacao_saldo(saldo_atual, saldo_anterior):
    """
    Calcula a variação percentual do saldo.
    """
    return calcular_variacao_percentual(
        saldo_atual,
        saldo_anterior
    )