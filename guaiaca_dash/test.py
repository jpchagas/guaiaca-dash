import pandas as pd
import os
from uploader import Uploader
import json
from pdf_extractor import PDFExtractor



pdfe = PDFExtractor()

#with open(os.getcwd() + '/guaiaca_dash/data_resume.json') as json_result:
#    parsed_json = json.load(json_result)



#u = Uploader()
#path = "/home/jpchagas/Downloads/guaiaca_dash/"
#folders = os.listdir(path)
#for folder in folders:
#    files = os.listdir(f'{path}{folder}/')
#    for file in files:
#        current_path_splitted = file.split("/")
#        file_name_extension = current_path_splitted[-1]
#        file_name,extension = file_name_extension.split(".")
#        bank,category,month = file_name.split("_")
                    #reader = PdfReader(uploaded_file)
                    #num_pages = len(reader.pages)
                    #all_text = ""
                    #for page_number in range(num_pages):
                    #    page = reader.pages[page_number] 
                    #    all_text += page.extract_text())
#        u.upload(f'{path}{folder}/{file}',None,bank,category,month,"jpchagas")

    #transactions_expected = parsed_json[bank][category][month]['transactions']
    #total_expected = parsed_json[bank][category][month]['total']

    #if round(df['valor'].sum(),2) == total_expected:
    #    print("Valor Total Bateu")
    #else:
    #    print("Valor Total Não Bateu")

    #if df.shape[0] == transactions_expected:
    #    print("Quantidade de transações bateu")
    #else:
    #    print("Quantidade de transações não bateu")




df_output = pd.read_csv(os.getcwd() + '/guaiaca_dash/data/output/jpchagas/maio.csv', sep=',')
print(df_output)
df_output['valor'] = pd.to_numeric(df_output['valor'])
grouped_sum = df_output.groupby('transacao')['valor'].sum().reset_index()
print(grouped_sum)

