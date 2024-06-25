import re
import pandas as pd
from string_helper import StringHelper

from pdf_extractor import PDFExtractor
from config import Config

from datetime import datetime

from filesystem import FileSystem

class BradescoBill:
    def __init__(self) -> None:        
        self.pdf_extractor = PDFExtractor()
        self.c = Config()
        self.sh = StringHelper()
        self.fl = FileSystem()

    def extract_info(self,file_path):
        pdf_data = self.pdf_extractor.extract_data(file_path)
        #combined_pattern = re.compile(f"({self.c.get_config('date_pattern')})|({self.c.get_config('date_pattern_year')})|({self.c.get_config('mistaken_pattern')})|({self.c.get_config('mistaken_pattern1')})")
        combined_pattern = re.compile("(^[0-9]+\/[0-9]+)|(^XXXX.XXXX.XXXX.[0-9]+\/[0-9]+\\D+)|(^[a-zA-Z]+\\**\\s*[a-zA-Z]*\\s*[0-9]+\/[0-9]+\\,[0-9]*)|(^[a-zA-z]+[0-9]+\\,[0-9]+)")
        data = [line for data in pdf_data for line in data if combined_pattern.match(line)]

        for i in range(len(data)):
            match = re.match('^XXXX.XXXX.XXXX.[0-9]{4}([0-9]{2}\/[0-9]{2}\s.+)',data[i])
            if match:
                data[i]=match.group(1)
        
        data1 = self.spit_data_description(data)
        data2 = self.concat_fraction_value(data1)
        data3 = self.clean_trash(data2)

        df = self.build_df(data3)

        return df

    def clean_trash(self, charges):
        delete_info = []
        for i in range(len(charges)):
            match = re.match('^([a-zA-Z]+\s?\D*)(\d{1,2}\/\d{1,2})?(\S\d+\,\d+)', charges[i])
            if match:
                charges[i-1] = f'{charges[i-1]} {match.group(1)} {match.group(2)} {match.group(3)}'
                delete_info.append(i)
        delete_info.sort(reverse=True)
        for i in delete_info:
            del charges[i]
        return charges

    def spit_data_description(self, charges):
        for i in range(len(charges)):
            match = re.match(self.c.get_config('digiopt1'), charges[i])
            if match:
                charges[i] = charges[i].replace(match.group(1),match.group(1)+' ')
        return charges

    def concat_fraction_value(self, charges):
        delete_info = []
        for i in range(len(charges)):
            match = re.match(self.c.get_config('digiopt2'), charges[i])
            if match:
                charges[i-1] = charges[i-1] + ' ' + charges[i].replace(match.group(1),match.group(1)+' ')
                delete_info.append(i)
        delete_info.sort(reverse=True)
        for i in delete_info:
            del charges[i]
        return charges
    
    def build_df(self,charges):
        charges_tuples = []

        for c in charges:
            c_splitted = c.split()

            # Determine the date
            data = c_splitted[0]
            if not re.match(self.c.get_config('date_pattern_year'), data):
                data += f"/{datetime.now().year}"
            
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
        df = df[~df['descricao'].isin(['PAGTO. POR DEB EM C/C', 'SALDO ANTERIOR'])]

        # Step 4: Split the 'parcela' column into 'parcela' and 'qt_parcelas'
        df[['parcela', 'qt_parcelas']] = df['parcela'].str.split('/', expand=True)
        df['qt_parcelas'] = df['qt_parcelas'].fillna('1')  # In case there is no fraction, assume '1'
        #df = df.drop(columns=['parcela'])

        # Step 5: Add constant columns
        df['transacao'] = 'despesa'
        df['metodo'] = 'cc'
        df['banco'] = 'bradesco'
        df['origem'] = ' '
        df['categoria'] = ' '
        return df
        