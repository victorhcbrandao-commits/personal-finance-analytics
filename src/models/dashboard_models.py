"""
==============================================================================
FinSight

Modelos de dados utilizados pelo Dashboard.
==============================================================================
"""

from dataclasses import dataclass
import pandas as pd


# ==============================================================================
# GASTOS
# ==============================================================================

@dataclass
class DadosGastos:

    top_despesas: pd.DataFrame
    top_receitas: pd.DataFrame
    categorias: pd.DataFrame
    cartoes: pd.DataFrame


# ==============================================================================
# DASHBOARD
# ==============================================================================

@dataclass
class DashboardData:

    gastos: DadosGastos