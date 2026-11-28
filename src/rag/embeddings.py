from langchain_huggingface import HuggingFaceEmbeddings
import torch

class embeddings:
    def __init__(self):
        self.device = "mps" if torch.mps.is_available() else "cpu"
        self.emedding_model = HuggingFaceEmbeddings(
            model_name = "BAAI/bge-m3",
            model_kwargs = {
                "device": self.device},
            
                encode_kwargs = {
                "normalize_embeddings": True
                }
            
        )
        
    def generate_embeddings(self,chunks):
        return self.emedding_model.embed_documents(chunks)
    
    
    def generate_query_embeddings(self,query):
        return self.emedding_model.embed_query(query)
