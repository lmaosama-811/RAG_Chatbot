from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGService:
    def __init__(self,chunk_size,chunk_overlap):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    def load_pdf(self,file,embeddings,question):
        chunks = self.text_splitter.split_documents(file)
        vectorstore = FAISS.from_documents(chunks,embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k":4})
        docs = retriever.invoke(question)
        return "\n".join([doc.page_content for doc in docs])

rag_service = RAGService(1000,200)