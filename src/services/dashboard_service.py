"""
==============================================================================
FinSight

Dashboard Service

Responsável por preparar dados derivados utilizados pelo dashboard.
==============================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from src.analysis import (
    maiores_despesas,
    maiores_receitas,
    gastos_por_categoria,
    despesas_por_cartao
)

from src.utils import formatar_moeda

from src.models.dashboard_models import (
    DashboardData,
    DadosGastos
)


# ==============================================================================
# GASTOS
# ==============================================================================

def preparar_gastos_dashboard(df):
    top_despesas = maiores_despesas(df)

    top_despesas["valor_formatado"] = (
        top_despesas["valor"]
        .apply(formatar_moeda)
    )

    top_receitas = maiores_receitas(df)

    top_receitas["valor_formatado"] = (
        top_receitas["valor"]
        .apply(formatar_moeda)
    )

    categorias = gastos_por_categoria(df)

    cartoes = despesas_por_cartao(df)

    cartoes["valor_formatado"] = (
        cartoes["valor"]
        .apply(formatar_moeda)
    )

    return DadosGastos(
    top_despesas=top_despesas,
    top_receitas=top_receitas,
    categorias=categorias,
    cartoes=cartoes
)


# ==============================================================================
# DASHBOARD PRINCIPAL
# ==============================================================================

def preparar_dashboard(df):

    return DashboardData(
        gastos=preparar_gastos_dashboard(df)
    )