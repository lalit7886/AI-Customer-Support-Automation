from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class chunking:
    def __init__(self):
        self.text_splitter= RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " "]
        )

        
    def chunker(self,document: Document | list[Document])->list[Document]:
        document = [document] if isinstance(document, Document) else document
        chunk = self.text_splitter.split_documents(document)
        
        return chunk
        
        
        
    
    
    