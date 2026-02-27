from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class ChatbotRequest(BaseModel):
    session_id: int|None=None
    file_id: str
    question: str 

class ConversationHistory(SQLModel, table=True):
    __tablename__="conversation_history"
    id:int|None = Field(default=None, primary_key=True)
    session_id: int
    session_name: str|None = None
    role: str
    content: str 

class Summary(SQLModel,table=True):
    __tablename__="summary"
    id: int|None = Field(default=None,primary_key=True)
    covered_until_message_id: int
    content: str 
