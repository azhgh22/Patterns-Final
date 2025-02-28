from playground.infra.currency_converter.er_api_converter import ErApiConverter


def test_should_convert_gel_to_usd() -> None:
    converter = ErApiConverter()
    try:
        converter.convert("BADRI", "GEL", 100)
    except ValueError:
        assert False
