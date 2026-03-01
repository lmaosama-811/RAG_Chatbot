from sqlmodel import create_engine, Session 
from .core.env_config import settings 

engine = create_engine(settings.database_url)

def get_session():
    with Session(engine) as session:
        yield session