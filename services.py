from api import resposta_get_api
import streamlit as st


@st.cache_data(ttl=60)
def buscar_cotacao(par_moeda, tipo="bid"):
    url_completa = f"last/{par_moeda}"

    dados = resposta_get_api(url_completa)

    if not dados:
        return None

    try:
        moedas_tratadas = par_moeda.replace("-", "")

        valor_cotacao = float(dados[moedas_tratadas][tipo])
        variacao = float(dados[moedas_tratadas]["pctChange"])

        return {
            "valor": valor_cotacao,
            "variacao": variacao
        }

    except (KeyError, ValueError, TypeError):
        return None


def converter(valor, cotacao):
    return (valor * cotacao)


def registrar_historico(moeda, valor, tipo, resultado):
    registro = {
        "moeda": moeda,
        "valor": valor,
        "tipo": tipo,
        "resultado": resultado
    }

    return registro


@st.cache_data(ttl=60 * 10)
def obter_historico_moeda(par, dias):
    endpoint = f"daily/{par}/{dias}"
    
    dados = resposta_get_api(endpoint)

    if dados:
        return dados
    
    return []