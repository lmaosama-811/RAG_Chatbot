import os
from .service.PDF_service import pdf_service

def check_file_available(file_name):
    file_path = pdf_service.get_file_path(file_name)
    if not os.path.isfile(file_path):
        return None 

def check_file_type(file):
    return file.filename.lower().endswith(".pdf")