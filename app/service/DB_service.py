from sqlmodel import select,update, delete,desc

from ..schemas.request_model import ConversationHistory, Summary

class DBService:
    def clean_text(self,text: str) -> str:
        if text is None:
            return text
        return text.replace("\x00", "")
    def get_conversation_history(self,session_id:int, db):
        cmd = select(ConversationHistory.role, ConversationHistory.content).where(ConversationHistory.session_id == session_id)
        return db.exec(cmd).all() #return tuple as we selecting columns
    def get_last_dialog(self,session_id,db)-> ConversationHistory|None:
        cmd = select(ConversationHistory).where(ConversationHistory.session_id == session_id).order_by(desc(ConversationHistory.id)).limit(1)
        return db.exec(cmd).first()
    def create_dialog(self, session_id, session_name, role, content,db):
        clean_content = self.clean_text(content)
        new_diaglog = ConversationHistory(session_id=session_id,session_name=session_name,role=role,content=clean_content)
        db.add(new_diaglog)
        db.commit()
    def update_dialog_name(self,session_id,new_name,db):
        cmd = update(ConversationHistory.session_name).where(ConversationHistory.session_id==session_id).values(session_name=new_name)
        db.exec(cmd)
        db.commit()
    def delete_conversation(self,session_id,db):
        cmd= delete(ConversationHistory).where(ConversationHistory.session_id == session_id)
        db.exec(cmd)
        db.commit()
    def get_list_conversation(self,db):
        cmd = select(ConversationHistory.session_id,ConversationHistory.session_name)
        return db.exec(cmd).all()
    def get_conversation(self,session_id,db):
        cmd = select(ConversationHistory).where(ConversationHistory.session_id==session_id)
        return db.exec(cmd).first() #ConversationHistory|None 
    def create_summary(self,covered_until_message_id,content,db): #summary table
        clean_content = self.clean_text(content)
        new_summary = Summary(covered_until_message_id=covered_until_message_id,content=clean_content)
        db.add(new_summary)
        db.commit()
    def get_last_summary(self, session_id, db):
        cmd = select(Summary).where(Summary.session_id == session_id)\
                            .order_by(desc(Summary.id))\
                            .limit(1)
        return db.exec(cmd).first()

db_service = DBService()
