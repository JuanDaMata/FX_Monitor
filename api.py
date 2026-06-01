import requests

URL_BASE = "https://economia.awesomeapi.com.br/json/"


def resposta_get_api(endpoint):
    url_completa = URL_BASE + endpoint

    try:
        resposta = requests.get(url_completa, timeout=10)

        resposta.raise_for_status()

        return resposta.json()

    except requests.RequestException as e:
        print(f"Erro na API: {e}")
        return None
