import streamlit as st

from services import buscar_cotacao
from utils.constantes import (
    PARES_DISPONIVEIS,
    TIPOS_COTACOES_DISPONIVEIS
)


@st.cache_data(ttl=60)
def buscar_cotacao_cached(par, tipo):
    return buscar_cotacao(par, tipo)


def renderizar_cotacoes():
    st.title("💸 Gestão de Cotações Financeiras")
    st.divider()

    tipo_cotacao = st.selectbox(
        "Selecione o tipo de cotação:",
        TIPOS_COTACOES_DISPONIVEIS,
        index=0,
        key="tipo_cotacao_exibir"
    )

    st.divider()
    st.info(f"Carregando as cotações {tipo_cotacao}...")


    for i in range(0, len(PARES_DISPONIVEIS), 3):

        grupo_moedas = PARES_DISPONIVEIS[i:i+3]
        cols = st.columns(3)

        for col, par in zip(cols, grupo_moedas):

            cotacao = buscar_cotacao_cached(par, tipo_cotacao)
            moeda_base = par.split("-")[0]

            with col:
                if cotacao:
                    st.metric(
                        label=f"Cotação {moeda_base}:",
                        value=f"R$ {cotacao['valor']:.4f}",
                        delta=f"{cotacao['variacao']:.2f}%"
                    )
                else:
                    st.metric(
                        label=f"Cotação {moeda_base}:",
                        value="N/D"
                    )
                    st.error(f"Falha ao carregar: {par}")

    st.divider()
    st.info(f"Valor {tipo_cotacao} fornecido pela AwesomeAPI.")