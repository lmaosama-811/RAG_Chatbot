from fastapi import HTTPException 

class LLMService: 
    def __init__(self): 
        self.system_message = {"summarization":{"role":"system","ntent":"You are a talent summarization assistant"}, 
                               "question_answer":{"role":"system","content":"You are a talent question answering assistant"}} 
    def format_user_content(self,task,context=None,question=None,conversation_history = None,old_summary=None):
            if task not in self.system_message: 
                raise HTTPException(400,"Chatbot doesn't support this task") 
            with open(f"app/prompt/{task}.text", "r") as f: 
                raw_content = f.read() 
            if task == "question_answer": 
                return (raw_content.replace("<<CONTEXT>>",context).replace("<<QUESTION>>",question))
            return (raw_content.replace("<<MESSAGES>>",conversation_history).replace("<<OLDSUMMARY>>",old_summary))
        
    def ask_model(self,llm,task,user_content,conversation_history=[]):
            prompt = [self.system_message[task]] + conversation_history + [{"role":"","content":user_content}]
            try: 
                return llm.invoke(prompt) 
            except TimeoutError: 
                raise HTTPException(504,"LLM timeout") 
            
llm_service = LLMService()
