from langchain_community.vectorstores import FAISS
from langchain_experimental.text_splitter import SemanticChunker
from sentence_transformers import CrossEncoder 
import os
import logging

from .PDF_service import pdf_service 
from ..model import embeddings
from ..core.env_config import settings 

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self,embeddings):
        self.text_splitter = SemanticChunker(embeddings=embeddings)
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    def rerank(self,query,documents,top_k=5):
        pairs = [(query,doc.page_content) for doc in documents] #create pair (query,doc)
        scores = self.reranker.predict(pairs) #predict scores 
        scored_docs = list(zip(documents,scores)) 
        scored_docs.sort(key=lambda x:x[1], reverse=True) #sort descending
        return [doc for doc,_ in scored_docs[:top_k]] #List[Document]
    def load_pdf(self,file_id,file,embeddings,question):
        logger.info("Start processing PDF", extra={"file_id": file_id})

        file_path = pdf_service.get_file_path("indexes",file_id)
        if os.path.exists(file_path):
            vectorstore = FAISS.load_local(file_path, embeddings,allow_dangerous_deserialization=True)
            logger.info("FAISS index loaded successfully")
        else:
            chunks = self.text_splitter.split_documents(file)
            logger.info("Text split completed",extra={"chunks": len(chunks)})

            vectorstore = FAISS.from_documents(chunks,embeddings)
            vectorstore.save_local(file_path)
            logger.info("FAISS index saved")

        retriever = vectorstore.as_retriever(search_kwargs={"k":settings.top_k}) #Create wrapper object surrounding FAISS => save k, save search type and prepare for search (NOT search)
        docs = retriever.invoke(question) #get k chunks with highest similarity -> Measure vector distance -> List[Document]
        logger.info("Documents retrieved")
        
        reranked_docs = self.rerank(question,docs) #List[Document]
        return "\n".join([doc.page_content for doc in reranked_docs])

rag_service = RAGService(embeddings)