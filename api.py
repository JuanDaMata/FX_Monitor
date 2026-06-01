import requests

URL_BASE = "https://economia.awesomeapi.com.br/json/"

def resposta_get_api(endpoint):
    url = URL_BASE + endpoint

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        return resposta.json()

    except requests.Timeout:
        return None

    except requests.RequestException:
        return None