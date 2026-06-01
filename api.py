import requests

URL_BASE = "https://economia.awesomeapi.com.br/json/"

CACHE = {}
    
def resposta_get_api(endpoint):
    url_completa = URL_BASE + endpoint

    try:
        resposta = requests.get(url_completa, timeout=10)
        resposta.raise_for_status()

        data = resposta.json()
        CACHE[endpoint] = data
        return data

    except requests.Timeout:
        return {"erro": "timeout"}

    except requests.RequestException:
        return {"erro": "falha_api"}