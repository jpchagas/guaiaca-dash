import pandas as pd

class CSVExtractor:
    def __init__(self) -> None:
        pass

    def extract_data(self,file_path):
        return pd.read_csv(file_path,sep=";")
    
    def extract_data_comma(self, file_path):
        return pd.read_csv(file_path,sep=",")