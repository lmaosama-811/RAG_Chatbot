from fastapi import HTTPException 

class LLMService: 
    def __init__(self): 
        self.system_message = {"summarization":{"role":"system","ntent":"You are a talent summarization assistant"}, 
                               "question_answer":{"role":"system","content":"You are a talent question answering assistant"}} 
    def format_prompt(self,task,context=None,question=None,conversation_history = None,old_summary=None):
            if task not in self.system_message: 
                raise HTTPException(400,"Chatbot doesn't support this task") 
            with open(f"app/prompt/{task}.text", "r") as f: 
                raw_content = f.read() 
            if task == "question_answer": 
                user_content= (raw_content.replace("<<CONTEXT>>",context).replace("<<QUESTION>>",question))
                prompt = [self.system_message[task]] + conversation_history + [{"role":"","content":user_content}]
            else:
                user_content = (raw_content.replace("<<MESSAGES>>",conversation_history).replace("<<OLDSUMMARY>>",old_summary))
                prompt = [self.system_message[task]] + [{"role":"user","content":user_content}]
        return prompt 
    def ask_model(self,prompt,llm):
            try: 
                return llm.invoke(prompt) 
            except TimeoutError: 
                raise HTTPException(504,"LLM timeout") 
            
llm_service = LLMService()
