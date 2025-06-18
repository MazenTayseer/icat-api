import re
from dataclasses import dataclass

from django.conf import settings
from ollama import Client

from apps.dal.models.enums.ai_roles import AIRole


@dataclass
class OllamaMessage:
    role: str
    content: str

    def __post_init__(self):
        if self.role not in AIRole.get_all_roles():
            raise ValueError(f"Invalid role: {self.role}")

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }


class OllamaClient:
    def __init__(self):
        self.client = Client(host=settings.OLLAMA_HOST)

    def __strip_md_fence(self, text: str) -> str:
        """Remove ``` fences if present."""
        pattern = r"^```(?:json)?\s*(.*?)\s*```$"
        m = re.match(pattern, text.strip(), re.DOTALL | re.IGNORECASE)
        return m.group(1) if m else text

    def chat(self, messages: list[OllamaMessage]):
        response = self.client.chat(
            model=settings.OLLAMA_MODEL,
            messages=[message.to_dict() for message in messages],
            stream=False,
        )
        return self.__strip_md_fence(response["message"]["content"])
