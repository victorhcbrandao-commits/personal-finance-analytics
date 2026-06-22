import streamlit as st

from components.card_kpi import card_kpi


def card_fire(
    patrimonio_objetivo,
    percentual_independencia,
    anos_faltantes,
    formatar_moeda
):

    col1, col2, col3 = st.columns(3)

    with col1:

        card_kpi(
            "Patrimônio FIRE",
            formatar_moeda(
                patrimonio_objetivo
            ),
            "🔥",
            "#EF4444"
        )

    with col2:

        card_kpi(
            "Progresso FIRE",
            f"{percentual_independencia:.1f}%",
            "📈",
            "#F59E0B"
        )

    with col3:

        card_kpi(
            "Anos Restantes",
            f"{anos_faltantes:.1f}",
            "🗓️",
            "#8B5CF6"
        )

    largura_fire = max(
        percentual_independencia,
        3
    )

    st.subheader(
        "Progresso para Independência Financeira"
    )

    st.markdown(
        f"""
<div style='width:100%; height:16px; background-color:#1f2937; border-radius:8px;'>

<div style='width:{largura_fire}%; height:16px; background-color:#EF4444; border-radius:8px;'>
</div>

</div>

<div style='margin-top:12px; color:#9ca3af;'>
{percentual_independencia:.2f}% concluído
</div>
""",
        unsafe_allow_html=True
    )