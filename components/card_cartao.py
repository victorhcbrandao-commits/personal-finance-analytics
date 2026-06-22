import streamlit as st


def card_cartao(linha, formatar_moeda):

    valor_fatura = linha["valor"]
    limite_total = linha["limite"]
    limite_disponivel = limite_total - valor_fatura

    percentual_utilizado = (
        valor_fatura / limite_total
    ) * 100

    largura_barra = max(
        percentual_utilizado,
        3
    )

    cores_cartoes = {
        "Black Visa": "#F59E0B",
        "Black Master": "#EF4444",
        "Azul Platinum": "#2563EB"
    }

    cor_cartao = cores_cartoes.get(
        linha["cartao"],
        "#3B82F6"
    )

    st.markdown(
        f"""
<div style='background-color:#111827; border:1px solid #1f2937; border-radius:16px; padding:20px; min-height:290px;'>
    <div style='font-size:20px; font-weight:700; color:white;'>💳 {linha["apelido"]}</div>
    <div style='color:#9ca3af; margin-top:8px;'>🏦 {linha["banco"]}</div>
    <div style='font-size:28px; font-weight:700; color:white; margin-top:20px; white-space:nowrap;'>{formatar_moeda(linha["valor"])}</div>
    <div style='color:#9ca3af; margin-top:18px;'>{percentual_utilizado:.1f}% utilizado</div>
    <div style='width:100%; height:10px; background-color:#1f2937; border-radius:8px; margin-top:10px;'><div style='width:{largura_barra}%; height:10px; background-color:{cor_cartao}; border-radius:8px;'></div></div>
    <div style='color:#9ca3af; margin-top:18px;'>Limite disponível</div>
    <div style='font-size:18px; color:#00CC96; font-weight:700;'>{formatar_moeda(limite_disponivel)}</div>
    <div style='color:#9ca3af; margin-top:20px;'>📅 Vencimento: dia {linha["vencimento"]}</div>
    <div style='color:#9ca3af; margin-top:8px;'>💳 {linha["bandeira"]}</div>
</div>
        """,
        unsafe_allow_html=True
    )