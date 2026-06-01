from unittest.mock import patch
from services import buscar_cotacao


@patch("services.resposta_get_api")
def test_busca_cotacao(mock_api):

    mock_api.return_value = {
        "USDBRL": {
            "bid": "5.50",
            "pctChange": "1.20"
        }
    }

    resultado = buscar_cotacao("USD-BRL")

    assert resultado == {
        "valor": 5.5,
        "variacao": 1.2
    }


@patch("services.resposta_get_api")
def test_busca_cotacao_sem_retorno(mock_api):

    mock_api.return_value = None

    resultado = buscar_cotacao("USD-BRL")

    assert resultado is None