from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.services.ingestion_service import generate_hash


class chunking:
    def __init__(self):
        self.text_splitter= RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " "]
        )


        
    def chunker(self,document: Document | list[Document])->list[Document]:
        document = [document] if isinstance(document, Document) else document
        chunks = self.text_splitter.split_documents(document)
        for each_chunk in chunks:
            each_chunk.metadata["chunk_hash"]=generate_hash(each_chunk.page_content)
            each_chunk.metadata["chunk_id"]=f'{each_chunk.metadata.get("document_id")}_{each_chunk.metadata.get("chunk_hash")[:16]}'
        
        return chunks
        
        
        
    
    
    