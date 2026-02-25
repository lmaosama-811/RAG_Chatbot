from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_key:str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    ) #Pydantic v2

settings = Settings()

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    api_key= settings.api_key,
    base_url="https://openrouter.ai/api/v1"
)

llm = ChatOpenAI(
    model="openai/gpt-4o",
    api_key= settings.api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=1000
)

