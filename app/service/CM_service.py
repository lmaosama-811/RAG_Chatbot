from .LLM_service import llm_service
from .DB_service import db_service

class ConversationManagement:
    def __init__(self):
        self.summarization = {"role":"system"}
        self.token_threshold = 6000
    def format_history(self,dialog:tuple):
        return {"role":dialog[0],"content":dialog[1]}
    def load_conversation_history_and_update_summarization(self,session_id,db,llm,old_summary=None):
        dialogs = db_service.get_conversation_history(session_id,db)
        count = 0
        recent_dialogs = []
        for i in range(len(dialogs),-1,-1):
            if count < self.token_threshold:
                recent_dialogs.append(self.format_history(dialogs[i]))
                count += (len(dialogs[i][1]) + 3)
            else:
                sum_list = []
                for j in range(i+1):
                    sum_list.append(self.format_history(dialogs[j]))
                summary = llm_service.ask_model(task="summarization",llm=llm,conversation_history=sum_list,old_summary=old_summary)
                db_service.create_summary(i+1,summary,db)
                break 
        return recent_dialogs, {**self.summarizaton,**{"content":summary}} # list[role,content] and role,content
    
CM_service = ConversationManagement()
        

            
