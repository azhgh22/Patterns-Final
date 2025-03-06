
import requests


class ErApiConverter:
    def __init__(self) -> None:
        url = "https://open.er-api.com/v6/latest/GEL"
        response = requests.get(url)
        data = response.json()
        self.rates = data.get("rates", {})

    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch currency rates.")

        data = response.json()
        rates = data.get("rates", {})

        if to_currency not in rates:
            raise IndexError(f"Currency {to_currency.upper()} is not supported.")

        conversion_rate = float(rates[to_currency])
        return amount * conversion_rate
