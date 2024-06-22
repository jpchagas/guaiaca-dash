from csv_extractor import CSVExtractor

class NubankStatement:
    def __init__(self) -> None:
        self.csv_extractor = CSVExtractor()
    
    def extract_info(self, file_path):
        df = self.csv_extractor.extract_data_comma(file_path)
        df = df[["Data", "Valor", "Descrição"]]
        df = df[df['Descrição'] != 'Pagamento de fatura']
        df['Valor'] = df['Valor'].abs()
        df['transacao']=['receita' if x>0 else 'despesa' for x in df['Valor']]
        df['metodo'] = 'pix ou transferencia'
        df['banco'] = 'nubank'
        df['parcela'] = 1
        df['qt_parcelas'] = 1
        df = df.rename(columns={
            "Data": "data",
            "Descrição": "descricao",
            "Valor": "valor"
        })
        return df