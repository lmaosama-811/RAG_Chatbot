from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

from .PDF_service import pdf_service 

class RAGService:
    def __init__(self,chunk_size,chunk_overlap):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    def load_pdf(self,file_id,file,embeddings,question):
        file_path = pdf_service.get_file_path("indexes",file_id)
        if os.path.exists(file_path):
            vectorstore = FAISS.load_local(file_path, embeddings,allow_dangerous_deserialization=True)
        else:
            chunks = self.text_splitter.split_documents(file)
            vectorstore = FAISS.from_documents(chunks,embeddings)
            vectorstore.save_local(file_path)
        retriever = vectorstore.as_retriever(search_kwargs={"k":4})
        docs = retriever.invoke(question)
        return "\n".join([doc.page_content for doc in docs])

rag_service = RAGService(1000,200)