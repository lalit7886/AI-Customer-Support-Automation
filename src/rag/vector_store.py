from pinecone import Pinecone, ServerlessSpec
from src.core.config import get_settings
from src.core.logging import logger
from src.core.exceptions import MyException
import time
from langchain_core.documents import Document

settings = get_settings()


class pinecone_service:
    def __init__(self):
        self.pc=Pinecone(
            api_key=settings.pinecone_api_key,
    
            
        )
        
        self.index=None
    def ensure_index(self):
        if settings.pinecone_index_name not in [x["name"] for x in self.pc.list_indexes()]:
            logger.info(f"creating pinecone index")
            self.pc.create_index(
                name=settings.pinecone_index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws",region="us-east-1")
            )
            
        while not self.pc.describe_index(settings.pinecone_index_name).status["ready"]:
            logger.info(f"waiting for the index to be ready")
            time.sleep(1)
        
        self.index = self.pc.Index(settings.pinecone_index_name)

        
    def upsert(self,chunks,emb):
        '''
        chunks: list of chunks
        emb: list of embeddings
        '''
        logger.info(f"starting the upsert in vector database.")
        
        if len(chunks) != len(emb):
            raise ValueError("The lenght of chunks and embedding vector must be same")
        self.ensure_index()
        for chunk,emb_ in zip(chunks,emb):
            self.index.upsert(
                vectors=[{
                    "id":chunk.metadata.get("chunk_id"),
                    "values":emb_,
                    "metadata":chunk.metadata
                }],
                namespace=settings.pinecone_namespace
            )
            
        logger.info(f"Successfully saved the embeddings in vector database.")
        
        
    def similarity_search(self,query_embedding,top_k=settings.top_k,filter=None):
        try:
            logger.info(f"Running simiarity search")
            if self.index is None:
                self.ensure_index()
            
            response = self.index.query(vector=query_embedding,
                                        top_k=top_k,
                                        include_metadata=True,
                                        namespace=settings.pinecone_namespace,
                                        filter=filter)
            documents = []
            for matches in response.matches:
                logger.info("Getting matches")
                metadata=dict(matches.metadata or {})
                
                text_content = metadata.pop("text", None)
                
                if not text_content:
                    logger.warning(f"misssing content for vecotr id {matches.id}")
                    
                    continue
                metadata["score"]=matches.score
                documents.append(Document(
                    page_content=text_content,
                    metadata=metadata
                ))
                
            logger.info(f"Retrieved document of length {len(documents)}")
            return documents
        
        except Exception as e:
            raise MyException(e) from e
            
if __name__ == "__main__":
    from src.rag.embeddings import embeddings
    emb=embeddings()
    
    # # ps=pinecone_service()
    text="What is the price of accurate entry?"

    result = emb.generate_query_embeddings(text)
  

    print("Result type:", type(result))
    print("Result shape:", getattr(result, "shape", None))
    print("Result length:", len(result))

 