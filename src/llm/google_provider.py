from src.core.logging import logger
from src.core.exceptions import MyException
from src.core.config import get_settings
from src.llm.base import BaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI

Settings = get_settings()

class Gemini_provider(BaseLLM):
    def __init__(self):
        logger.info("initiating Gemini_provider")
        self.model = Settings.gemini_model
        self.client=ChatGoogleGenerativeAI(api_key=Settings.gemini_api_key,model=self.model,
                                      temperature=0.1,
                                      max_retries=3)
        
    def generate_response(self, prompt):
        if not prompt or not prompt.strip():
            raise ValueError(f"The prompt cant be empty")
        
        try:
            logger.info("Generating response")
            response = self.client.invoke(prompt)
            
            final_response = response.content[0]["text"]
            if not isinstance(final_response,str):
                raise TypeError(f"The response by llm is not of type string")
            logger.info(f"response is generated succesfully")
            return final_response
        except Exception as e:
            raise MyException(e) from e
        
if __name__ == "__main__":
    gemini_provider = Gemini_provider()
    prompt = "What is the capital of France?"
    response=gemini_provider.generate_response(prompt)
    print(response)
            
        
        