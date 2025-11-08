from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

class VectorStoreManager:
    def __init__(self, api_key: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vectorstore = None
    
    def build_index(self, scraped_data: List[Dict[str, str]]):
        print("\nBuilding vector index...")
        
        documents = []
        for item in scraped_data:
            if item['content']:
                doc = Document(
                    page_content=item['content'],
                    metadata={'source': item['url'], 'title': item['title']}
                )
                documents.append(doc)
        
        if not documents:
            raise ValueError("No documents to index")
        
        # split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks from {len(documents)} documents")
        
        # build vector store
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        print("Index built successfully")
    
    def search(self, query: str, k: int = 4) -> List[Document]:
        if not self.vectorstore:
            return []
        return self.vectorstore.similarity_search(query, k=k)
