import streamlit as st


def card_kpi(
    titulo,
    valor,
    icone,
    cor,
    subtitulo=None,
    variacao=None,
    cor_variacao="#22C55E"
):
    subtitulo_html = subtitulo if subtitulo else ""

    variacao_html = (
        f"<div style='font-size:13px; font-weight:700; color:{cor_variacao}; margin-top:6px;'>{variacao}</div>"
        if variacao
        else ""
    )

    html = (
        f"<div style='background-color:#111827; padding:18px; border-radius:18px; border:1px solid #1f2937; height:145px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 4px 14px rgba(0,0,0,0.20);'>"
        f"<div style='display:flex; justify-content:space-between; align-items:flex-start;'>"
        f"<span style='font-size:14px; color:#cbd5e1; font-weight:600; white-space:normal; line-height:1.3;'>{titulo}</span>"
        f"<span style='width:34px; height:34px; display:flex; align-items:center; justify-content:center; background-color:#1f2937; border-radius:10px; font-size:18px;'>{icone}</span>"
        f"</div>"
        f"<div>"
        f"<div style='font-size:24px; font-weight:800; color:{cor}; white-space:nowrap; line-height:1.2;'>{valor}</div>"
        f"{variacao_html}"
        f"<div style='font-size:12px; color:#94a3b8; margin-top:4px; min-height:16px; white-space:normal; line-height:1.2;'>{subtitulo_html}</div>"
        f"</div>"
        f"</div>"
    )

    st.markdown(html, unsafe_allow_html=True)