class LLMService:
    def __init__(self):
        with open("app/prompt.txt", "r") as f:
            self.content = f.read()
    def ask_model(self,context,question,llm):
        prompt = (self.content.replace("<<CONTEXT>>", context).replace("<<QUESTION>>", question))
        answer = llm.invoke(prompt)
        return answer 
    
llm_service = LLMService()