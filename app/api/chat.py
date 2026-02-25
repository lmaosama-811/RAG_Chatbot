from fastapi import APIRouter
from typing import Union

from ..schemas.request_model import *
from ..schemas.response_model import *
from ..model import embeddings, llm
from ..service.RAG_service import rag_service
from ..service.LLM_service import llm_service
from ..service.PDF_service import pdf_service
from ..deps import check_file_available

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("",response_model=Union[ChatBotResponse,Message])
def chat(request: ChatbotRequest):
    """Select the file you would like the chatbot to retrieve information from (by entering file name), and enter the question you wish to ask.\n
    You can check whether the file exists by Get Files"""
    if check_file_available(request.file_name) is None:
        return Message(message="File not Found")
    file = pdf_service.get_file(request.file_name)
    context = rag_service.load_pdf(file,embeddings,request.question)
    output = llm_service.ask_model(context,request.question,llm)
    return ChatBotResponse(model_name="GPT-4o",answer=output.content,count=len(output.content.split()))

