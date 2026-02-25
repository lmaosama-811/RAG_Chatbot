import os 
from langchain_community.document_loaders import PyPDFLoader

class PDFService:
    def __init__(self):
        self.upload_dir = "data/upload"
        os.makedirs(self.upload_dir,exist_ok=True)
    def save_file(self,file_bytes, file_name):
        file_path = os.path.join(self.upload_dir,file_name)
        with open(file_path,"wb") as f:
            f.write(file_bytes)
        return file_path
    def get_file_path(self,file_name):
        return os.path.join(self.upload_dir,file_name)
    def get_file(self,file_name):
        loader = PyPDFLoader(self.get_file_path(file_name))
        return loader.load()
    def get_list_file(self):
        return [f for f in os.listdir(self.upload_dir) if f.endswith(".pdf")]
    
pdf_service = PDFService()
