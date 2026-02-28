from .LLM_service import llm_service
from .DB_service import db_service

import uuid 

class ConversationManagement:
    def __init__(self):
        self.summarization = {"role":"system"}
        self.token_threshold = 6000
    def format_history(self,dialog:tuple): #return conversation history 
        return {"role":dialog[0],"content":dialog[1]}
    def load_conversation_history_and_update_summarization(self,session_id,db,llm,index=None,old_summary=None):
        dialogs = db_service.get_conversation_history(session_id,db) #get all dialogs
        count = 0
        recent_dialogs = []
        for i in range(len(dialogs),-1,-1):
            if (count + len(dialogs[i][1].split())+3) <= self.token_threshold:
                recent_dialogs.append(self.format_history(dialogs[i]))
                count += (len(dialogs[i][1].split()) + 3)
            else:
                sum_list = []
                for j in range(i+1):
                    sum_list.append(self.format_history(dialogs[j]))
                if len(sum_list) !=0:
                    user_content = llm_service.format_user_content(task="summarization",conversation_history=sum_list,old_summary=old_summary)
                    summary = llm_service.ask_model(llm,user_content)
                    db_service.create_summary(i+1,summary,db) #base 1 according to table 
                    return recent_dialogs+[{**self.summarizaton,**{"content":summary}}] # list[role,content] and role,content
        return recent_dialogs #list(role,content)
    def analyze_conversation_history(self,session_id,db,llm,user_content):
        old_summary = db_service.get_last_summary(db) #Summary
        if old_summary is None:
            return self.load_conversation_history_and_update_summarization(session_id,db,llm)
        dialogs_for_summary = (db_service.get_conversation_history(session_id,db)[old_summary.covered_until_message_id -1,old_summary.covered_until_message_id +5)
                               #nếu độ dài từ old_summary 
    def generate_session_id(self):
        return uuid.uuid4().hex[:16]
    
CM_service = ConversationManagement()
        

            
