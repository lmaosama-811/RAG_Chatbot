import os
from .service.PDF_service import pdf_service
from .service.DB_service import db_service 

def check_file_available(file_id):
    file_path = pdf_service.get_file_path("upload",file_id)
    return os.path.isfile(file_path) 

def check_file_type(file):
    return file.filename.lower().endswith(".pdf")

def check_session_id_available(session_id,db):
    if session_id is None:
        return True   # cho phép tạo session mới
    conversation = db_service.get_conversation(session_id, db)
    return conversation is not None
