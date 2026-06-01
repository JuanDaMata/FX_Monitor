import streamlit as st
import pandas as pd

from services import obter_historico_moeda
from utils.constantes import (
    MOEDAS_DISPONIVEIS,
    PARES_SUPORTADOS,
    TIPOS_COTACOES_DISPONIVEIS
)


@st.cache_data(ttl=600)
def obter_historico_cached(par, dias):
    return obter_historico_moeda(par, dias)


def renderizar_grafico():
    st.title("📈 Gráfico cotação")
    st.divider()

    dias_disponiveis = [7, 15, 30, 60, 90, 180, 360]

    tipo_cotacao = st.selectbox(
        "Selecione o tipo de cotação:",
        TIPOS_COTACOES_DISPONIVEIS,
        index=0,
        key="tipo_cotacao_grafico"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        moeda_origem = st.selectbox(
            "Moeda de Origem:",
            MOEDAS_DISPONIVEIS,
            index=1,
            key="moeda_origem_grafico"
        )

    with col2:
        moeda_destino = st.selectbox(
            "Moeda de Destino:",
            PARES_SUPORTADOS[moeda_origem],
            index=0,
            key="moeda_destino_grafico"
        )

    with col3:
        dias_anteriores = st.selectbox(
            "Quantos dias atrás?",
            dias_disponiveis,
            index=0,
            key="dias_disponiveis_grafico"
        )

    mostrar_grafico_btn = st.button("Mostrar Gráfico")

    if mostrar_grafico_btn:

        st.divider()
        st.info("Carregando gráfico...")

        par_moeda_grafico = f"{moeda_origem}-{moeda_destino}"

        historico_variacao = obter_historico_cached(
            par_moeda_grafico,
            dias_anteriores
        )

        if not historico_variacao:
            st.warning("Não foi possível carregar o histórico da API.")
            return

        data_frame = pd.DataFrame(historico_variacao)

        if data_frame.empty:
            st.warning("Dados vazios da API.")
            return

        if tipo_cotacao not in data_frame.columns:
            st.error(f"Coluna '{tipo_cotacao}' não encontrada nos dados da API.")
            st.write(data_frame.columns)
            return

        data_frame[tipo_cotacao] = pd.to_numeric(
            data_frame[tipo_cotacao],
            errors="coerce"
        )

        data_frame["timestamp"] = pd.to_datetime(
            data_frame["timestamp"].astype(int),
            unit="s"
        )

        data_frame = data_frame.set_index("timestamp")
        data_frame.index = data_frame.index.strftime("%d/%m/%Y")

        st.line_chart(data_frame[tipo_cotacao])

        st.divider()

        with st.expander("Visualizar histórico em tabela"):

            tabela = data_frame.reset_index()[["timestamp", tipo_cotacao]]

            tabela = tabela.rename(columns={
                "timestamp": "Data",
                tipo_cotacao: f"Valor {tipo_cotacao.upper()}"
            })

            st.dataframe(
                tabela,
                hide_index=True,
                width="stretch"
            )