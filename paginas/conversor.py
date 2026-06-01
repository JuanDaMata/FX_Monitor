import streamlit as st

from services import (
    buscar_cotacao,
    converter,
    registrar_historico
)

from utils.constantes import (
    MOEDAS_DISPONIVEIS,
    PARES_SUPORTADOS,
    TIPOS_COTACOES_DISPONIVEIS
)


@st.cache_data(ttl=60)
def buscar_cotacao_cached(par_moeda, tipo):
    return buscar_cotacao(par_moeda, tipo)


def renderizar_conversor():
    st.set_page_config(layout="centered")

    st.title("🔄 Gestão de Cotações Financeiras")
    st.divider()

    if "historico" not in st.session_state:
        st.session_state.historico = []

    tipo_cotacao = st.selectbox(
        "Selecione o tipo de cotação:",
        TIPOS_COTACOES_DISPONIVEIS,
        index=0,
        key="tipo_cotacao_converter"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        moeda_origem = st.selectbox(
            "Moeda de Origem:",
            MOEDAS_DISPONIVEIS,
            index=1
        )

    with col2:
        moeda_destino = st.selectbox(
            "Moeda de Destino:",
            PARES_SUPORTADOS[moeda_origem],
            index=0
        )

    with col3:
        valor_para_converter = st.number_input(
            label="Digite o valor a converter:",
            min_value=1.00
        )

    buscar_cotacao_btn = st.button("Buscar Cotação")

    if buscar_cotacao_btn:
        try:
            st.info(
                f"Buscando a cotação {tipo_cotacao} de {moeda_origem.upper()} → {moeda_destino.upper()}..."
            )

            par_moedas = f"{moeda_origem}-{moeda_destino}"

            cotacao = buscar_cotacao_cached(par_moedas.upper(), tipo_cotacao)

            if not cotacao:
                st.error("Cotação indisponível no momento.")
                st.stop()

            valor_convertido = converter(
                valor_para_converter,
                cotacao["valor"]
            )

            st.divider()
            st.subheader("Resultado Da Conversão:")

            if valor_para_converter > 1:
                st.success(
                    f"{valor_para_converter} **{moeda_origem}** Valem → **{valor_convertido:.4f} {moeda_destino}**"
                )
            else:
                st.success(
                    f"{valor_para_converter} **{moeda_origem}** Vale → **{valor_convertido:.4f} {moeda_destino}**"
                )

            st.divider()
            st.info(f"Valor {tipo_cotacao} fornecido pela AwesomeAPI.")

            registro = registrar_historico(
                par_moedas,
                valor_para_converter,
                tipo_cotacao,
                valor_convertido
            )

            st.session_state.historico.append(registro)

        except Exception as e:
            st.error(f"Erro na conversão: {e}")

    st.divider()

    with st.expander("Visualizar conversões realizadas"):
        st.subheader("Histórico:")

        if not st.session_state.historico:
            st.info("Nenhuma conversão realizada até o momento.")
        else:
            dados = []

            for item in st.session_state.historico:
                origem, destino = item["moeda"].split("-")

                dados.append({
                    "Origem": origem,
                    "Destino": destino,
                    "Valor": item["valor"],
                    "Convertido": f"({item['tipo']}) {round(item['resultado'], 4)}"
                })

            st.dataframe(dados, width="stretch")

        if st.button("Limpar Histórico"):
            st.session_state.historico = []
            st.rerun()