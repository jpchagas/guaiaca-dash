from pypdf import PdfReader

class PDFExtractor:
    def __init__(self) -> None:
        pass

    def extract_data(self, file_path):
        reader = PdfReader(file_path)
        return [page.extract_text().splitlines() for page in reader.pages]
     