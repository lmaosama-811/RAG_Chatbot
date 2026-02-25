from pydantic import BaseModel, Field

class Message(BaseModel):
    message:str

class Error(BaseModel):
    code: int
    error: str

class ChatBotResponse(BaseModel):
    model_name: str
    answer: str
    count: int = Field(gt=0)