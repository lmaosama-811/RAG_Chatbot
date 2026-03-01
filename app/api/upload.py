from fastapi import APIRouter, UploadFile, File 
from typing import Union
import logging 

from ..schemas.response_model import Message, Error
from ..service.PDF_service import pdf_service
from ..deps import check_file_type, validate_file_size

router = APIRouter(prefix ="/upload", tags=["Upload File"])
logger = logging.getLogger(__name__)

@router.post("", response_model=Union[Message,Error])
async def upload_file(file: UploadFile = File()):
    """Upload PDF file. This chatbot only support PDF file!"""
    logger.info("Upload request received")
    if not check_file_type(file):
        logger.warning("Invalid file upload attempt")
        return Error(code=400,error=f"Invalid file. This chatbot only support PDF file!")
    if validate_file_size(file):
        logger.warning("File is too large")
        return Message(message="File is too large")
    content = await file.read()
    file_id = pdf_service.save_file(content, file.filename)
    return Message(message =f"You have upload file {file.filename} successfully! File ID: {file_id}") 

@router.get("/list")
def get_files():
    """Check list of file that you have uploaded"""
    return pdf_service.get_list_file()
