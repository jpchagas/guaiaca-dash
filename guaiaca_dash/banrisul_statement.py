import re
import pandas as pd
from string_helper import StringHelper
from date_helper import DateHelper
from pdf_extractor import PDFExtractor
from config import Config

from datetime import datetime


class BanrisulStatement:
    def __init__(self) -> None:
        self.pdf_extractor = PDFExtractor()
        self.c = Config()
        self.sh = StringHelper()
        self.dh = DateHelper()

    def extract_info(self,file_path):
        pdf_data = self.pdf_extractor.extract_data(file_path)
        # Combine patterns into a single pattern using alternation
        combined_pattern = re.compile(f"({self.c.get_config('banrisul_pattern')})|({self.c.get_config('banrisul_pattern_2')})")
        # Use list comprehension to filter lines that match any of the combined patterns
        charges = [line for data in pdf_data for line in data if combined_pattern.match(line)]
        data = ""
        descricao = ""
        valor = 0
        transacao = ""
        month_number = ""
        year = ""
        tuples = []
        for c in charges:
            match_data = re.match('\+\+\s*MOVIMENTOS\s+(\w+)\/(\d{4})',c)
            match_transaction = re.match('^(\d*)\s+(\D+)\s+\d+\s+(\d+\,\d+)(\-*)', c)
            if match_data:
                print
                month_number = self.dh.get_month_number_abbr(match_data.group(1))
                year = match_data.group(2)
            elif match_transaction:
                if match_transaction.group(1) != '':
                    data = f'{match_transaction.group(1)}/{month_number}/{year}'
                descricao = match_transaction.group(2)
                valor = match_transaction.group(3)
                if match_transaction.group(4) == '':
                    transacao = "receita"
                else:
                    transacao = "despesa"
                tuples.append((data,descricao,float(self.sh.convert_brazil_to_us_currency(valor)),transacao))
        df = pd.DataFrame(tuples, columns =['data', 'descricao', 'valor','transacao'])
        df['metodo'] = 'pix ou transferencia'
        df['banco'] = 'banrisul'
        df['parcela'] = '1'
        df['qt_parcelas'] = '1'
        df['origem'] = ' '
        df['categoria'] = ' '
        return df
