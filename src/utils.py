def formatar_moeda(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

def calcular_variacao_percentual(valor_atual, valor_anterior):
    if valor_anterior == 0 or valor_anterior is None:
        return None

    variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100

    if variacao > 0:
        return {
            "texto": f"▲ +{variacao:.1f}%",
            "cor": "#22C55E",
            "valor": variacao,
            "tipo": "positivo"
        }

    elif variacao < 0:
        return {
            "texto": f"▼ {variacao:.1f}%",
            "cor": "#EF553B",
            "valor": variacao,
            "tipo": "negativo"
        }

    return {
        "texto": "▬ 0.0%",
        "cor": "#94A3B8",
        "valor": 0,
        "tipo": "neutro"
    }