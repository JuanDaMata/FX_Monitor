import requests

URL_BASE = "https://economia.awesomeapi.com.br/json/"


def resposta_get_api(endpoint):
    url_completa = URL_BASE + endpoint
    resposta = requests.get(url_completa)

    if resposta.status_code == 200:
        return resposta.json()
    
    return {}
