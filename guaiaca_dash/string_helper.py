class StringHelper:
    def __init__(self) -> None:
        pass

    def convert_brazil_to_us_currency(self,brazil_currency):
        # Remove any dots used as thousand separators
        brazil_currency_no_thousand_sep = brazil_currency.replace('.', '')
        # Replace the comma used as a decimal separator with a dot
        us_currency = brazil_currency_no_thousand_sep.replace(',', '.')
        return us_currency