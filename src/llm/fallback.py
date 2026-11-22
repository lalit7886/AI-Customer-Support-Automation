
from typing import Sequence

from src.core.logging import logger
from src.core.exceptions import MyException
from src.llm.base import BaseLLM


class FallbackModel(BaseLLM):

    def __init__(
        self,
        primary: BaseLLM,
        fallback: Sequence[BaseLLM]
    ):
        self.primary_model = primary
        self.fallback = list(fallback)

    def generate_response(self, prompt: str) -> str:

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty or whitespace.")

        llm_providers = [self.primary_model, *self.fallback]

        last_error: Exception | None = None

        for provider in llm_providers:

            try:
                logger.info(
                    "Generating response using %s",
                    provider.__class__.__name__
                )

                response = provider.generate_response(prompt)

                if not isinstance(response, str) or not response.strip():
                    raise ValueError(
                        f"{provider.__class__.__name__} generated an empty response."
                    )

                logger.info(
                    "Successfully generated response using %s",
                    provider.__class__.__name__
                )

                return response

            except Exception as e:
                logger.exception(
                    "Provider %s failed.",
                    provider.__class__.__name__
                )
                last_error = e

        raise MyException(last_error) from last_error


if __name__ == "__main__":

    from src.llm.groq_provider import Groq_provider

    primary_model = Groq_provider()

    fallback_model = FallbackModel(
        primary=None,
        fallback=[primary_model]
    )

    prompt = "Who are you? Aren't you Groq?"

    response = fallback_model.generate_response(prompt)

    print(response)
