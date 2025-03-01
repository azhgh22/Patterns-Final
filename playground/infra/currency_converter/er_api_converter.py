import requests


class ErApiConverter:
    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        url = "https://open.er-api.com/v6/latest/GEL"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch currency rates.")

        data = response.json()
        rates = data.get("rates", {})

        if to_currency not in rates:
            raise IndexError(f"Currency {to_currency.upper()} is not supported.")

        conversion_rate = float(rates[to_currency])
        return amount * conversion_rate
