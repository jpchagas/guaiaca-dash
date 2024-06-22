import os

class FileSystem:
    def __init__(self) -> None:
        self.cfp = os.getcwd() + "/guaiaca_dash/data/output/" #/home/jpchagas/Documents/Projects/guaiaca-dash

    def folder_existence(self, user):
        folder_path = f"{self.cfp}{user}"
        if os.path.isdir(folder_path):
            return True
        else:
            return False
            

    def file_existence(self, user, bank, month):
        file_path = f"{self.cfp}{user}/{month}.csv"
        if os.path.isfile(file_path):
            return True
        else:
            return False
        
    def create_folder(self, user):
        folder_path = f"{self.cfp}{user}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
        else:
            print(f"Folder '{folder_path}' already exists.")
    
    def get_filepath(self, user):
        return f"{self.cfp}{user}"

