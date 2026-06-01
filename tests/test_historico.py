from unittest.mock import patch

from services import (
    registrar_historico,
    obter_historico_moeda
)


def test_registrar_historico():
    resultado = registrar_historico(
        "USD-BRL",
        100,
        "bid",
        550
    )

    assert resultado == {
        "moeda": "USD-BRL",
        "valor": 100,
        "tipo": "bid",
        "resultado": 550
    }


@patch("services.resposta_get_api")
def test_obter_historico_com_dados(mock_api):

    mock_api.return_value = [
        {
            "bid": "5.50",
            "ask": "5.52"
        }
    ]

    resultado = obter_historico_moeda(
        "USD-BRL",
        1
    )

    assert resultado == [
        {
            "bid": "5.50",
            "ask": "5.52"
        }
    ]


@patch("services.resposta_get_api")
def test_obter_historico_vazio(mock_api):

    mock_api.return_value = None

    resultado = obter_historico_moeda(
        "USD-BRL",
        1
    )

    assert resultado == []