import streamlit as st


def card_kpi(
    titulo,
    valor,
    icone,
    cor
):

    st.markdown(
        f"""
<div style='background-color:#111827; padding:20px; border-radius:16px; border:1px solid #1f2937; min-height:120px;'>

<div style='display:flex; justify-content:space-between; align-items:center;'>

<span style='font-size:16px; color:#cbd5e1;'>
{titulo}
</span>

<span style='font-size:20px;'>
{icone}
</span>

</div>

<div style='font-size:24px; font-weight:700; color:{cor}; margin-top:18px; white-space:nowrap;'>

{valor}

</div>

</div>
        """,
        unsafe_allow_html=True
    )