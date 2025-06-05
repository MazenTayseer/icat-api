from django.conf import settings
from ollama import Client


class OllamaClient:
    def __init__(self):
        self.client = Client(host=settings.OLLAMA_HOST)

    def chat(self, role: str, content: str):
        return self.client.chat(
            model=settings.OLLAMA_MODEL,
            messages=[{"role": role, "content": content}],
            stream=False,
        )
