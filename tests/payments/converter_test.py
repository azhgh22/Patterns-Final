from playground.infra.currency_converter.er_api_converter import ErApiConverter


def test_should_convert_gel_to_usd() -> None:
    converter = ErApiConverter()
    ans = converter.convert("GEL", "USD", 100)
    assert ans == 100 * converter.rates["USD"]
