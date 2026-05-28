import streamlit as st
import pandas as pd

from services import obter_historico_moeda

from utils.constantes import (
    MOEDAS_DISPONIVEIS,
    PARES_SUPORTADOS,
    TIPOS_COTACOES_DISPONIVEIS
)

def renderizar_grafico():
    st.set_page_config(layout = "centered")
    st.title("📈 Gráfico cotação")
    st.divider()


    dias_disponiveis = [7, 15, 30, 60, 90, 180, 360]

    tipo_cotacao = st.selectbox(
        "Selecione o tipo de cotação: '**bid**' para valor de compra e '**ask**' para valor de venda",
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
            "Quantos dias Atrás?",
            dias_disponiveis,
            index=0,
            key="dias_disponiveis_grafico"
        )
    
    mostrar_grafico_btn = st.button("Mostrar Gráfico")


    if mostrar_grafico_btn:
        st.divider()
        st.info("Carregando gráfico...")
        st.divider()

        st.info(
            "Passe o mouse sobre o gráfico para visualizar os valores de cada data."
        )

        par_moeda_grafico = f"{moeda_origem}-{moeda_destino}"

        historico_variacao = obter_historico_moeda(par_moeda_grafico, dias_anteriores)

        data_frame = pd.DataFrame(historico_variacao)

        data_frame[tipo_cotacao] = data_frame[tipo_cotacao].astype(float)

        data_frame["timestamp"] = pd.to_datetime(
            data_frame["timestamp"].astype(int),
            unit="s"
        )

        data_frame = data_frame.set_index("timestamp")

        data_frame.index = data_frame.index.strftime("%d/%m/%Y")

        st.line_chart(data_frame[tipo_cotacao])

    st.divider()
    with st.expander("Visualizar histórico em tabela"):
        st.subheader(
            f"Variação de {moeda_origem} → {moeda_destino} nos últimos {dias_anteriores} dias"
        )

        st.info(
            f"Carregando histórico {tipo_cotacao} dos ultimos {dias_anteriores}..."
        )

        par_moeda_grafico = f"{moeda_origem}-{moeda_destino}"

        historico_variacao = obter_historico_moeda(par_moeda_grafico, dias_anteriores)

        data_frame = pd.DataFrame(historico_variacao)

        data_frame[tipo_cotacao] = data_frame[tipo_cotacao].astype(float)

        data_frame["timestamp"] = pd.to_datetime(
            data_frame["timestamp"].astype(int),
            unit="s"
        )

        data_frame["timestamp"] = data_frame["timestamp"].dt.strftime("%d/%m/%Y")


        tabela_filtrada = data_frame[["timestamp", tipo_cotacao]]

        tabela_filtrada = tabela_filtrada.rename(columns={
            "timestamp": "Data",
            tipo_cotacao: f"Valor {tipo_cotacao.upper()}"
        })


        st.dataframe(
            tabela_filtrada,
            width="stretch",
            hide_index=True
        )