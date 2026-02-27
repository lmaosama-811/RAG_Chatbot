from sqlmodel import create_engine, Session 

engine = create_engine("postgresql+psycopg://postgres:ghasdfgh.09.za@localhost:8117/Conversation History",echo = True) #Chuyển tạm vào model và sửa tên database (nếu không connect được)

def get_session():
    with Session(engine) as session:
        yield session