import streamlit as st
from bradesco_bill import BradescoBill
from banrisul_statement import BanrisulStatement
from c6_bill import C6Bill
from c6_statement import C6Statement
from digio_bill import DigioBill
from caixa_statement import CaixaStatement
from nubank_bill import NubankBill
from nubank_statement import NubankStatement
import pandas as pd
from filesystem import FileSystem

from logger import ColoredLogger

class Uploader:
    def __init__(self) -> None:
        self.bradesco_fatura = BradescoBill()
        self.banrisul_extrato = BanrisulStatement()
        self.c6_fatura = C6Bill()
        self.c6_extrato = C6Statement()
        self.digio_fatura = DigioBill()
        self.caixa_extrato = CaixaStatement()
        self.nubank_fatura = NubankBill()
        self.nubank_extrato = NubankStatement()
        self.fl = FileSystem()
        self.logger = ColoredLogger(__name__)

    def upload(self,file,extension,bank,category,month,user):
        match bank:
            case "bradesco":
                if category == 'fatura':
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.bradesco_fatura.extract_info(file)
                    self.save_file(user,bank,month,df)
                else:
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                return st.success(f'{category} do {bank} de {month} foi importado')
            case "banrisul":
                if category == 'fatura':
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                else:
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.banrisul_extrato.extract_info(file)
                    self.save_file(user,bank,month,df)
                return st.success(f'{category} do {bank} de {month} foi importado')
            case "caixa":
                if category == 'fatura':
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                else:
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.caixa_extrato.extract_info(file)
                    self.save_file(user,bank,month,df)
                return st.success(f'{category} do {bank} de {month} foi importado')
            case "digio":
                if category == 'fatura':
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.digio_fatura.extract_info(file)
                    self.save_file(user,bank,month,df)
                else:
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                return st.success(f'{category} do {bank} de {month} foi importado')
            case "c6":
                if category == 'fatura':
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.c6_fatura.extract_info(file)
                    self.save_file(user,bank,month,df)
                else:
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.c6_extrato.extract_info(file)
                    self.save_file(user,bank,month,df)
                return st.success(f'{category} do {bank} de {month} foi importado')
            case "nubank":
                if category == 'fatura':
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.nubank_fatura.extract_info(file)
                    self.save_file(user,bank,month,df)
                else:
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                    df = self.nubank_extrato.extract_info(file)
                    self.save_file(user,bank,month,df)
                return st.success(f'{category} do {bank} de {month} foi importado')
            case "btg":
                if category == 'fatura':
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                else:
                    self.logger.info(f"Importando dados de {category} do {bank} de {month}")
                return st.success(f'{category} do {bank} de {month} foi importado')
            case _:
                self.logger.info(f"Banco não cadastrado")
                return st.error("Banco não cadastrado")
            
    def save_file(self,user,bank,month,df):
        file_path = self.fl.get_filepath(user)
        if self.fl.folder_existence(user):
            if self.fl.file_existence(user, bank, month):
                output_df = pd.read_csv(f'{file_path}/{month}.csv')
                df_combined = pd.concat([output_df, df],ignore_index=False)
                df_combined = df_combined.drop_duplicates()
                saved = df_combined.to_csv(f'{file_path}/{month}.csv',index=False)
                if saved is not None:
                    return True
                else:
                    return True
            else:
                saved = df.to_csv(f'{file_path}/{month}.csv',index=False)
                if saved is None:
                    return True
                else:
                    return True
        else:
            self.fl.create_folder(user)
            if self.fl.file_existence(user, bank, month):
                output_df = pd.read_csv(f'{file_path}/{month}.csv')
                df_combined = pd.concat([output_df, df],ignore_index=False)
                df_combined = df_combined.drop_duplicates()
                saved = df_combined.to_csv(f'{file_path}/{month}.csv',index=False)
                if saved is not None:
                    return True
                else:
                    return True
            else:
                saved = df.to_csv(f'{file_path}/{month}.csv',index=False)
                if saved is None:
                    return True
                else:
                    return True