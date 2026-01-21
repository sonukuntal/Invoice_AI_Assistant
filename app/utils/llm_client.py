import ollama
from app.config import LLM_MODEL_NAME
from app.utils import get_logger

logger = get_logger(__name__)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        client = ollama.Client(host="http://127.0.0.1:11434")
        response = client.chat(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        logger.exception("LLM call failed")
        raise
