import os
from .core.env_config import settings 
from .service.PDF_service import pdf_service
from .service.DB_service import db_service 

def check_file_available(file_id):
    file_path = pdf_service.get_file_path("upload",file_id)
    return os.path.isfile(file_path) 

def check_file_type(file):
    return file.filename.lower().endswith(".pdf")

def check_session_id_available(session_id,db):
    return db_service.get_conversation(session_id, db) is not None 

def validate_file_size(file, max_file_size=settings.max_file_size):
    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > max_file_size:
            return True 
    return False 
    