from src.core.logging import logger
from src.core.exceptions import MyException
from uuid import uuid4
from src.services.ingestion_service import (
    extract_docx,
    extract_pdf,
    extract_readme,
    extract_text,
    generate_hash
)
from src.rag.embeddings import embeddings
from src.rag.vector_store import pinecone_service
from langchain_core.documents import Document
from src.rag.chunking import chunking
from pathlib import Path
from datetime import datetime



class Document_Ingestion:
    def __init__(self):
        self.extracted_text = None
        self.chunks=[]
        self.chunk = chunking()
        self.embedding = embeddings()
        self.vector_store = pinecone_service()
    
    def start_ingestion(self,file_path):
        logger.info(f'starting data ingestion of data {file_path}')
        try:
            # Extracting plain text
            file_type = Path(file_path).suffix.lower()
            if file_type == ".txt":
                self.extracted_text = extract_text(file_path)
            elif file_type == ".pdf":
                self.extracted_text = extract_pdf(file_path)
            elif file_type == ".docx":
                self.extracted_text = extract_docx(file_path)
            elif file_type == ".md":
                self.extracted_text = extract_readme(file_path)
            
            self.extracted_text = Document(page_content=self.extracted_text.get("extracted_text"),
                                           metadata={
                                                    "chunk_content":self.extracted_text.get("extracted_text"),
                                                  "document_id":str(uuid4()),
                                                  "document_hash":generate_hash(self.extracted_text.get("extracted_text")),
                                                  
                                                  "file_name":self.extracted_text.get("file_name"),
                                                  "source":self.extracted_text.get("source"),
                                                  "last_extracted_time":self.extracted_text.get("last_extracted_time")
                                           })
            #  Start chunking
            chunks=self.chunk.chunker(self.extracted_text) # type of chunk is list[Documents]
            
            # Generate Embeddings
            document_embeddings = self.embedding.generate_embeddings([chunk.page_content for chunk in chunks])
            
            # Vector Store
            self.vector_store.upsert(chunks,document_embeddings)

            logger.info("Successfully completed vector data ingestison")
            
        except Exception as e:
            raise MyException(e) from e
        
if __name__ == "__main__":
    ing = Document_Ingestion()
    ing.start_ingestion("knowledge_base/raw/free.docx")
        