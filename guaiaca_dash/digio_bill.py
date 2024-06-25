import re
import pandas as pd
from datetime import datetime
from string_helper import StringHelper

from pdf_extractor import PDFExtractor
from config import Config


class DigioBill:
    def __init__(self) -> None:
        self.pdf_extractor = PDFExtractor()
        self.c = Config()
        self.sh = StringHelper()

    def extract_info(self,file_path):
        pdf_data = self.pdf_extractor.extract_data(file_path)
        combined_pattern = re.compile(f"({self.c.get_config('date_pattern')})|({self.c.get_config('date_pattern_year')})|({self.c.get_config('mistaken_pattern')})")
        data = [line for data in pdf_data for line in data if combined_pattern.match(line)]
        return self.build_df(data)
    
    def build_df(self,charges):
        charges_tuples = []

        for c in charges:
            c_splitted = c.split()
            
            # Determine the date
            data = c_splitted[0]
            if not re.match(self.c.get_config('date_pattern_year'), data):
                data += f"/{datetime.now().year}"
            
            # Determine the amount
            amount = c_splitted[-1]
            
            # Determine the description and fraction
            if re.match(self.c.get_config('fraction_pattern'), c_splitted[-2]):
                fraction = c_splitted[-2]
                description = " ".join(c_splitted[1:-2])
            else:
                fraction = ""
                description = " ".join(c_splitted[1:-1])
            
            # Append to the list of tuples
            charges_tuples.append((data, description, fraction, float(self.sh.convert_brazil_to_us_currency(amount))))

        # Step 2: Create DataFrame from tuples
        df = pd.DataFrame(charges_tuples, columns=['data', 'descricao', 'parcela', 'valor'])

        # Step 3: Drop unwanted rows based on description
        df = df[~df['descricao'].isin(['Inclusao Pgto fatura QRCode'])]

        # Step 4: Split the 'parcela' column into 'parcela' and 'qt_parcelas'
        df[['parcela', 'qt_parcelas']] = df['parcela'].str.split('/', expand=True)
        df['qt_parcelas'] = df['qt_parcelas'].fillna('1')  # In case there is no fraction, assume '1'
        #df = df.drop(columns=['parcela'])

        # Step 5: Add constant columns
        df['transacao'] = 'despesa'
        df['metodo'] = 'cc'
        df['banco'] = 'digio'
        df['origem'] = ' '
        df['categoria'] = ' '
        return df