from csv_extractor import CSVExtractor
from string_helper import StringHelper

class C6Bill:
    def __init__(self) -> None:
        self.csv_extractor = CSVExtractor()
        self.sh = StringHelper

    def extract_info(self, file_path):
        df = self.csv_extractor.extract_data(file_path)
        df = df[["Data de Compra", "Descrição", "Parcela", "Valor (em R$)"]]
        df = df[df['Descrição'] != 'Pagamento Fatura QR CODE']
        df = df[df['Descrição'] != 'Inclusao de Pagamento    ']
        df[['parcela', 'qt_parcelas']] = df['Parcela'].str.split('/', expand=True)
        df = df.drop(columns=['Parcela'])
        df['transacao'] = 'despesa'
        df['metodo'] = 'cc'
        df['banco'] = 'c6'
        df = df.rename(columns={
            "Data de Compra": "data",
            "Descrição": "descricao",
            "Valor (em R$)": "valor"
        })
        return df