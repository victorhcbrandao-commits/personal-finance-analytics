import streamlit as st
from math import ceil


def card_meta(
    linha,
    patrimonio,
    aporte_mensal,
    formatar_moeda,
    calcular_meses_meta
):

    meses_para_meta = calcular_meses_meta(
        linha["objetivo"],
        patrimonio,
        aporte_mensal
    )

    meses_para_meta = ceil(
        meses_para_meta
    )

    if meses_para_meta == 0:
        previsao_meta = "✅ Já atingida"
    else:
        previsao_meta = f"🗓️ Faltam {meses_para_meta} meses"

    largura_barra = max(
        linha["percentual"],
        3
    )

    st.markdown(
        f"""
<div style='background-color:#111827; border:1px solid #1f2937; border-radius:16px; padding:20px; min-height:220px;'>
    <div style='font-size:22px; font-weight:700; color:white;'>🎯 {linha["meta"]}</div>
    <div style='color:#9ca3af; margin-top:15px;'>{formatar_moeda(linha["atual"])} / {formatar_moeda(linha["objetivo"])}</div>
    <div style='font-size:28px; font-weight:700; color:{linha["cor"]}; margin-top:20px;'>{linha["percentual"]:.1f}%</div>
    <div style='width:100%; height:10px; background-color:#1f2937; border-radius:8px; margin-top:15px;'><div style='width:{largura_barra}%; height:10px; background-color:{linha["cor"]}; border-radius:8px;'></div></div>
    <div style='color:#9ca3af; margin-top:18px;'>{previsao_meta}</div>
</div>
        """,
        unsafe_allow_html=True
    )