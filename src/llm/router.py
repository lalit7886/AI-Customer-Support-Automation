from src.llm.google_provider import Gemini_provider
from src.llm.groq_provider import Groq_provider
from src.llm.fallback import FallbackModel
from src.core.config import get_settings
from src.core.logging import logger
from src.core.exceptions import MyException


settings = get_settings()

class LLMroute:
    def __init__(self):
        self.primary_model = None
        self.secondary_models=list()
        self.fallback_model = None
    def _init_primary_model(self):
        self.primary_model = Groq_provider()
    
    def _init_fallback_model(self):
        Gemini_provider_ = Gemini_provider()
        self.secondary_models.append(Gemini_provider_)
        self.fallback_model=FallbackModel(self.primary_model,self.secondary_models)
    
    def generate_response(self,prompt:str):
        logger.info("LLM route for decision")
        try:
            self._init_primary_model()
            self._init_fallback_model()
            response = self.fallback_model.generate_response(prompt)
            logger.info("Response generated successfully")
            return response
        except Exception as e:
            raise MyException(e) from e
        
if __name__ == "__main__":
    llm_route = LLMroute()
    prompt = "What is the capital of France?"
    response = llm_route.generate_response(prompt)
    print(response)