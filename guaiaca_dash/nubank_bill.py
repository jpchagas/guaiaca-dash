import re
import pandas as pd
from string_helper import StringHelper
from date_helper import DateHelper

from pdf_extractor import PDFExtractor
from config import Config

from datetime import datetime

class NubankBill:
    def __init__(self) -> None:
        self.pdf_extractor = PDFExtractor()
        self.c = Config()
        self.sh = StringHelper()
        self.dh = DateHelper()

    def extract_info(self, file_path):
        charges = self.pdf_extractor.extract_data(file_path)
        charges_extracted = []
        for x in range(len(charges)):
            for y in range(len(charges[x])):
                if re.match('^([0-9]+)\s(\D+)$',charges[x][y]):
                    raw_data = charges[x][y].split()
                    data = f'{raw_data[0]}/{self.dh.get_month_number_abbr(raw_data[1].lower())}/{datetime.now().year}'
                    raw_description = charges[x][y+2].split("-")
                    descricao = raw_description[0]
                    parcela=""
                    qt_parcelas=""
                    if len(raw_description)>1:
                        parcela,qt_parcelas = raw_description[1].split("/")
                    valor = self.sh.convert_brazil_to_us_currency(charges[x][y+3])
                    charges_extracted.append((data,descricao,parcela,qt_parcelas,self.sh.convert_brazil_to_us_currency(valor)))
        df = pd.DataFrame(charges_extracted, columns =['data', 'descricao','parcela','qt_parcelas', 'valor'])
                # Step 3: Drop unwanted rows based on description
        df = df[~df['descricao'].str.contains("Pagamento em", case=False, na=False)]
        df['metodo'] = 'cc'
        df['banco'] = 'nubank'
        df['transacao'] = 'despesa'
        return df