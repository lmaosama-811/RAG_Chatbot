from fastapi import APIRouter, UploadFile, File 
from typing import Union

from ..schemas.response_model import Message, Error
from ..service.PDF_service import pdf_service
from ..deps import check_file_type

router = APIRouter(prefix ="/upload", tags=["Upload File"])

@router.post("", response_model=Union[Message,Error])
async def upload_file(file: UploadFile = File()):
    """Upload PDF file. This chatbot only support PDF file!"""
    if not check_file_type(file):
        return Error(code=400,error=f"Invalid file. This chatbot only support PDF file!")
    content = await file.read()
    file_id = pdf_service.save_file(content, file.filename)
    return Message(message =f"You have upload file {file.filename} successfully! File ID: {file_id}") 

@router.get("/list")
def get_files():
    """Check list of file that you have uploaded"""
    return pdf_service.get_list_file()
