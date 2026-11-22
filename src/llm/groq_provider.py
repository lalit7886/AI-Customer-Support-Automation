from src.core.exceptions import MyException
from src.core.logging import logger
from langchain_groq import ChatGroq
from src.llm.base import BaseLLM
from src.core.config import get_settings

setting = get_settings()

class Groq_provider(BaseLLM):
    def __init__(self):
        logger.info("initiating Groq_provider")
        if setting.groq_api_key is None:
            raise ValueError("OpenAI API key is not configured")
            
        self.model = setting.groq_llm_model
        self.client = ChatGroq(api_key=setting.groq_api_key,
                               model=self.model,
                              max_retries=setting.max_retries)
        
    def generate_response(self, prompt):
        try:
            logger.info("Generating response using Groq_provider")
            response = self.client.invoke(prompt)
            final_response = response.content
            if not isinstance(final_response,str):
                raise TypeError("Groq returned the type of not string")
            return final_response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise MyException(e) from e
        
        
if __name__ == "__main__":
    groq_provider = Groq_provider()
    prompt = "What is the capital of France?"
    response = groq_provider.generate_response(prompt)
    print(response)
        
