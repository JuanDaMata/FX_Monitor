from unittest.mock import patch
import requests
from api import resposta_get_api


@patch("api.requests.get")
def test_resposta_get_api_sucesso(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"bid": "5.10"}

    resultado = resposta_get_api("teste")

    assert resultado == {"bid": "5.10"}


@patch("api.requests.get")
def test_resposta_get_api_timeout(mock_get):
    mock_get.side_effect = requests.Timeout

    resultado = resposta_get_api("teste")

    assert resultado is None


@patch("api.requests.get")
def test_resposta_get_api_erro(mock_get):
    mock_get.side_effect = requests.RequestException

    resultado = resposta_get_api("teste")

    assert resultado is None