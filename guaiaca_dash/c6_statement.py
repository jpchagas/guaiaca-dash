from csv_extractor import CSVExtractor
import pandas as pd
from string_helper import StringHelper

class C6Statement:
    def __init__(self) -> None:
        self.csv_extractor = CSVExtractor()
        self.sh = StringHelper()

    def extract_info(self, file_path):
        df = self.csv_extractor.extract_data_comma(file_path)
        df = df[["data", "descricao", "valor", "transacao","metodo","banco","parcela","qt_parcelas"]]
        df['valor'] = df['valor'].apply(self.clean_valor)
        df['data'] = pd.to_datetime(df['data'])
        df['data'] = df['data'].dt.strftime('%d/%m/%Y')
        df = df[df['descricao'] != 'PGTOFATCARTAOC6-Faturadecartão']
        df['origem'] = ' '
        df['categoria'] = ' '
        return df
    
    def clean_valor(self, brazil_currency):
        # Remove any dots used as thousand separators
        brazil_currency_no_thousand_sep = brazil_currency.replace('.', '')
        # Replace the comma used as a decimal separator with a dot
        us_currency = brazil_currency_no_thousand_sep.replace(',', '.')
        return us_currency