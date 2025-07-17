from functools import lru_cache
from core.gemini_client import gemini_client

@lru_cache(maxsize=128)
def cached_response(prompt: str, task_type: str) -> str:
    return gemini_client.smart_call(prompt, task_type)
