import json
import re
from dataclasses import dataclass

from django.conf import settings
from google import genai

from apps.dal.models.enums.ai_roles import AIRole


@dataclass
class GeminiMessage:
    role: str
    content: str

    def __post_init__(self):
        if self.role not in AIRole.get_all_roles():
            raise ValueError(f"Invalid role: {self.role}")

    def to_dict(self):
        return {
            "role": self.role,
            "parts": [{"text": self.content}]
        }


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def __strip_md_fence(self, text: str) -> str:
        """Remove ``` fences if present."""
        pattern = r"^```(?:json)?\s*(.*?)\s*```$"
        m = re.match(pattern, text.strip(), re.DOTALL | re.IGNORECASE)
        return m.group(1) if m else text

    def chat(self, system_message: GeminiMessage | None, user_message: GeminiMessage):
        contents = [user_message.to_dict()]
        if system_message:
            contents.insert(0, system_message.to_dict())

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents
        )
        content = response.text

        if not content:
            raise ValueError("Response content is None")

        stripped_content = self.__strip_md_fence(content)
        try:
            return json.loads(stripped_content)
        except json.JSONDecodeError:
            return stripped_content

    def embed(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=settings.GEMINI_EMBEDDING_MODEL,
            contents=[text]
        )
        return response.embeddings[0].values
