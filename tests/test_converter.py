from services import converter

def test_converter_valor_inteiro():
    assert converter(100, 5.5) == 550


def test_converter_valor_zero():
    assert converter(0, 10) == 0


def test_converter_cotacao_inteira():
    assert converter(100, 5) == 500


def test_converter_valor_decimal():
    assert converter(10.5, 2) == 21