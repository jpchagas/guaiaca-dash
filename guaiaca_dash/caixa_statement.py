import re
import pandas as pd
from string_helper import StringHelper

from pdf_extractor import PDFExtractor
from config import Config

from datetime import datetime


class CaixaStatement:
    def __init__(self) -> None:
        self.pdf_extractor = PDFExtractor()
        self.c = Config()
        self.sh = StringHelper()
    
    def extract_info(self,file_path):
        pdf_data = self.pdf_extractor.extract_data(file_path)
        combined_pattern = re.compile(f"({self.c.get_config('date_pattern')})|({self.c.get_config('date_pattern_year')})|({self.c.get_config('mistaken_pattern')})")
        data = [line for data in pdf_data for line in data if combined_pattern.match(line)]
        charges_tuples=[]
        for c in data:
            c_splitted = c.split()
            data = c_splitted[0]
            description = ""
            for i in range(2,len(c_splitted)-2):
                    description += c_splitted[i]
            value = c_splitted[len(c_splitted)-2]
            transaction_type = c_splitted[len(c_splitted)-1]
            charges_tuples.append((data,description,float(self.sh.convert_brazil_to_us_currency(value)),transaction_type))
        df = pd.DataFrame(charges_tuples, columns =['data', 'descricao', 'valor','transacao'])
        df = df[df['descricao'] != 'SALDODIA']
        df = df.reset_index()
        df = df.drop(columns=['index'])
        df['transacao'] = ['despesa' if i == 'D' else 'receita' for i in df['transacao']]
        df['transacao'] = 'despesa'
        df['metodo'] = 'pix ou transferencia'
        df['banco'] = 'caixa'
        df['parcela'] = 1
        df['qt_parcelas'] = 1
        return df
