from fastapi import APIRouter, Depends,Request
from fastapi.responses import StreamingResponse
from sqlmodel import Session
import logging

from ..schemas.request_model import ChatbotRequest
from ..schemas.response_model import Message

from ..model import embeddings, llm
from ..service.RAG_service import rag_service
from ..service.LLM_service import llm_service
from ..service.PDF_service import pdf_service
from ..service.CM_service import CM_service
from ..service.DB_service import db_service
from ..deps import check_file_available,check_session_id_available
from ..db import get_session
from ..core.limiter import limiter

router = APIRouter(prefix="/chat", tags=["Chat"])
logger =logging.getLogger(__name__)

@router.post("")
@limiter.limit("10/minute") #10 request each minute each IP
def chat(request: Request,query: ChatbotRequest, db: Session = Depends(get_session)):
    """Select the file you would like the chatbot to retrieve information from (by entering file ID), and enter the question you wish to ask.\n
    You can check whether the file exists and file ID by Get Files\n
    Session name is automatically set to session ID.\n
    You can change it later"""
    logger.info("Chat request received",extra={"file_id": query.file_id})
    if not check_file_available(query.file_id):
        logger.warning("File not found", extra={"file_id": query.file_id})
        return Message(message="File not Found")
    if query.session_id is not None and not check_session_id_available(query.session_id,db):
        return Message(message="Session ID not Found")
    session_id = (CM_service.generate_session_id() if query.session_id is None else query.session_id)
    file =pdf_service.process_pdffile(query.file_id) 
    context = rag_service.load_pdf(query.file_id,file,embeddings,query.question) #Get k chunks
    #Load conversation history 
    conversation_history = CM_service.analyze_conversation_history(session_id,db,llm)
    #create dialog for role user in table 
    user_content = llm_service.format_user_content("question_answer",context,query.question)
    db_service.create_dialog(session_id,session_id,"user",user_content,db)
    def event_generator():
        try:
            full_response = ""
            for token in llm_service.ask_model(llm,"question_answer",user_content,conversation_history):
                full_response += token
                yield token
        finally:
            if full_response:
                db_service.create_dialog(session_id,session_id,"assistant",full_response,db)
    logger.info("Chat response generated")
    return StreamingResponse(event_generator(),media_type="text/plain")
    

