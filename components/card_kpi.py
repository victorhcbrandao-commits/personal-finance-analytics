import streamlit as st


def card_kpi(titulo, valor, icone, cor, subtitulo=None):
    subtitulo_html = subtitulo if subtitulo else ""

    html = f"""
<div style="background-color:#111827; padding:20px; border-radius:18px; border:1px solid #1f2937; min-height:135px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 4px 14px rgba(0,0,0,0.20);">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:14px; color:#cbd5e1; font-weight:500; white-space:nowrap;">{titulo}</span>
        <span style="width:34px; height:34px; display:flex; align-items:center; justify-content:center; background-color:#1f2937; border-radius:10px; font-size:18px;">{icone}</span>
    </div>
    <div>
        <div style="font-size:24px; font-weight:700; color:{cor}; margin-top:14px; white-space:nowrap; line-height:1.2;">{valor}</div>
        <div style="font-size:12px; color:#94a3b8; margin-top:6px; min-height:16px;">{subtitulo_html}</div>
    </div>
</div>
"""

    st.markdown(html, unsafe_allow_html=True)