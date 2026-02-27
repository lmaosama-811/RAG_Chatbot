import os
from .service.PDF_service import pdf_service

def check_file_available(file_id):
    file_path = pdf_service.get_file_path("upload",file_id)
    return os.path.isfile(file_path) 

def check_file_type(file):
    return file.filename.lower().endswith(".pdf")