import os


class PromptLoader:
    @staticmethod
    def load_prompt(file_path: str) -> str:
      prompts_dir = "common/prompts"
      file_path = os.path.join(prompts_dir, file_path)
      with open(file_path, 'r', encoding='utf-8') as file:
          return file.read()

class Prompts:
    INITIAL_ASSESSMENT = PromptLoader.load_prompt("initial_assessment.md")
    MODULE_ASSESSMENT = PromptLoader.load_prompt("module_assessment.md")
    PHISHING_SIMULATOR_PROMPT = PromptLoader.load_prompt("phishing_simulator.md")
    FALLBACK_PROMPT = PromptLoader.load_prompt("fallback.md")
