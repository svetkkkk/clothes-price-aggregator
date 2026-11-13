"""Currency Converter: перевод цен в единую валюту."""
from decimal import Decimal, ROUND_HALF_UP

# Сколько EUR стоит 1 единица валюты. В проде курсы берутся из внешнего API
# (например, ЕЦБ) и кэшируются раз в сутки; здесь статическая таблица.
DEFAULT_RATES = {
    "EUR": Decimal("1"),
    "USD": Decimal("0.92"),
    "GBP": Decimal("1.17"),
    "RUB": Decimal("0.0100"),
}


class UnknownCurrencyError(ValueError):
    pass


class CurrencyConverter:
    def __init__(self, rates=None):
        self.rates = dict(rates or DEFAULT_RATES)

    @property
    def supported(self):
        return sorted(self.rates)

    def _rate(self, code):
        code = code.upper()
        if code not in self.rates:
            raise UnknownCurrencyError(f"Неизвестная валюта: {code}")
        return self.rates[code]

    def convert(self, amount, from_cur, to_cur):
        result = Decimal(amount) * self._rate(from_cur) / self._rate(to_cur)
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
