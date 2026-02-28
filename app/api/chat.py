from fastapi import APIRouter, Depends
from typing import Union
from sqlmodel import Session

from ..schemas.request_model import ChatbotRequest
from ..schemas.response_model import ChatBotResponse, Message

from ..model import embeddings, llm
from ..service.RAG_service import rag_service
from ..service.LLM_service import llm_service
from ..service.PDF_service import pdf_service
from ..service.CM_service import CM_service
from ..service.DB_service import db_service
from ..deps import check_file_available,check_session_id_available
from ..db import get_session

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("",response_model=Union[ChatBotResponse,Message])
def chat(request: ChatbotRequest, db: Session = Depends(get_session)):
    """Select the file you would like the chatbot to retrieve information from (by entering file ID), and enter the question you wish to ask.\n
    You can check whether the file exists and file ID by Get Files\n
    Session name is automatically set to session ID."""
    if not check_file_available(request.file_id):
        return Message(message="File not Found")
    if not check_session_id_available(request.session_id,db):
        return Message(message="Session ID not Found")
    session_id = (CM_service.generate_session_id() if request.session_id is None else request.session_id)
    file =pdf_service.process_pdffile(request.file_id) 
    context = rag_service.load_pdf(request.file_id,file,embeddings,request.question) #Get k chunks
    #Load conversation history 
    conversation_history = CM_service.analyze_conversation_history(session_id,db,llm)
    #create dialog for role user in table 
    user_content = llm_service.format_user_content("question_answer",context,request.question)
    db_service.create_dialog(session_id,session_id,"user",user_content,db)
    output = llm_service.ask_model(llm,"question_answer",user_content,conversation_history)
    #create dialog for role assistant in table 
    db_service.create_dialog(session_id,session_id,"assistant",output.content,db)
    return ChatBotResponse(model_name="GPT-4o",session_id=session_id,session_name=session_id,answer=output.content,count=len(output.content.split())) 

