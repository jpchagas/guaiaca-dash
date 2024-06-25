import pandas as pd
import os
from uploader import Uploader
import json
from bradesco_bill import BradescoBill
from banrisul_statement import BanrisulStatement
from caixa_statement import CaixaStatement
from digio_bill import DigioBill
from nubank_bill import NubankBill


with open(os.getcwd() + '/guaiaca_dash/data_resume.json') as json_result:
    parsed_json = json.load(json_result)

bb = BradescoBill()
bs = BanrisulStatement()
cs = CaixaStatement()
db = DigioBill()
nb = NubankBill()

u = Uploader()
path = "/home/jpchagas/Downloads/guaiaca_dash/"
#folders = os.listdir(path)
folders = ['nubank']
for folder in folders:
    files = os.listdir(f'{path}{folder}/')
    for file in files:
        current_path_splitted = file.split("/")
        file_name_extension = current_path_splitted[-1]
        file_name,extension = file_name_extension.split(".")
        bank,category,month = file_name.split("_")

        df = None
        match folder:
            case "banrisul":
                df = bs.extract_info(f'{path}{folder}/{file}')
            case "caixa":
                df = cs.extract_info(f'{path}{folder}/{file}')
            case "bradesco":
                df = bb.extract_info(f'{path}{folder}/{file}')
            case "digio":
                df = db.extract_info(f'{path}{folder}/{file}')
            case "nubank":
                df = nb.extract_info(f'{path}{folder}/{file}')
            case _:
                pass
        print(f'Processando {category} do {bank} de {month}')
        try:
            transactions_expected = parsed_json[bank][category][month]['transactions']
            if df.shape[0] == transactions_expected:
                pass
            else:
                print(f'transações da extração {df.shape[0]} - transação esperado {transactions_expected}')
        except:
            print(f'{bank} não contabiliza transacoes')
            
        
        try:
            total_expected = parsed_json[bank][category][month]['total']
            total_calculated_calculated  = round(df['valor'].sum(),2)
            total_calculated_= df['valor'].sum()
            if round(df['valor'].sum(),2) == total_expected:
                pass
            else:
                print(f'total da extração {total_calculated_calculated} - total esperado {total_expected}')
                print(total_calculated_)
        except:
            print(f'{bank} não contabiliza valor')

            




#df_output = pd.read_csv(os.getcwd() + '/guaiaca_dash/data/output/jpchagas/maio.csv', sep=',')
#print(df_output)
#df_output['valor'] = pd.to_numeric(df_output['valor'])
#grouped_sum = df_output.groupby('transacao')['valor'].sum().reset_index()
#print(grouped_sum)

