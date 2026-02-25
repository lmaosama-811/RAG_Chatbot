from pydantic import BaseModel

class ChatbotRequest(BaseModel):
    file_name: str
    question: str 