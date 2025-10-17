from openai import OpenAI

LLM_API_BASE = "https://api.openai.com/v1"
LLM_API_KEY = "sk-proj-1234567890"
LLM_MODEL = "gpt-4o-mini"


class LLMWrapper:
    def __init__(self):
        self.client= OpenAI(base_url=LLM_API_BASE, api_key=LLM_API_KEY, max_retries=3)

    def generate_text(self, prompt, system_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        try:
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error while asking GPT: {e}")
            return None