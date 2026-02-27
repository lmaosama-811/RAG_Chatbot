from fastapi import APIRouter, Depend
from typing import Union
from sqlmodel import Session

from ..schemas.request_model import ChatbotRequest
from ..schemas.response_model import ChatBotResponse, Message

from ..model import embeddings, llm
from ..service.RAG_service import rag_service
from ..service.LLM_service import llm_service
from ..service.PDF_service import pdf_service
from ..service.CM_service import CM_service
from ..deps import check_file_available,check_session_id_available
from ..db import get_session

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("",response_model=Union[ChatBotResponse,Message])
def chat(request: ChatbotRequest, db: Session = Depend(get_session)):
    """Select the file you would like the chatbot to retrieve information from (by entering file ID), and enter the question you wish to ask.\n
    You can check whether the file exists and file ID by Get Files"""
    if not check_file_available(request.file_id):
        return Message(message="File not Found")
    if not check_session_id_available(request.session_id,db):
        return Message(message="Session ID not Found")
    if request.session_id is None:
        pass #create random session_id in CM_service 
    file =pdf_service.process_pdffile(request.file_id) 
    context = rag_service.load_pdf(request.file_id,file,embeddings,request.question) #Get k chunks
    #create dialog for role user in table 
    output = llm_service.ask_model(task="question_answer",llm=llm,context=context,question=request.question)
    #create dialog for role assistant in table 
    return ChatBotResponse(model_name="GPT-4o",answer=output.content,count=len(output.content.split())) #Adjust this 

