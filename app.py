import streamlit as st

from paginas.cotacoes import renderizar_cotacoes
from paginas.conversor import renderizar_conversor
from paginas.grafico import renderizar_grafico


st.set_page_config(layout="centered")

st.title("💰 Painel Financeiro")
st.divider()

aba_cotacao, aba_conversao, aba_grafico = st.tabs([
    "Cotação Moedas",
    "Conversor",
    "Gráfico Histórico"
])

with aba_cotacao:
    renderizar_cotacoes()

with aba_conversao:
    renderizar_conversor()

with aba_grafico:
    renderizar_grafico()