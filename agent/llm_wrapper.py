from openai import OpenAI

LLM_API_BASE = "https://api.openai.com/v1"
LLM_API_KEY = "sk-proj-1234567890"
LLM_MODEL = "gpt-4o-mini"

LLM_WRAPPER = LLMWrapper()

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

def get_split_prompt(word_limit=12):
    """
    num_parts: number of parts to split the sentence into
    word_limit: maximum number of words in each part
    """
    split_prompt = f"""
### Role
You are a professional Netflix subtitle splitter.

### Task
Split the given subtitle text into appropriate parts, each part less than {word_limit} words.

### Instructions
1. Maintain sentence meaning coherence according to Netflix subtitle standards
2. Keep parts roughly equal in length (minimum 3 words each)
3. Split at natural points like punctuation marks or conjunctions
4. It is necessary to use <br> for segmentation based on the semantics.
5. Directly return the segmented text without additional explanation.

### Examples
Input:
the upgraded claude sonnet is now available for all users developers can build with the computer use beta on the anthropic api amazon bedrock and google cloud’s vertex ai the new claude haiku will be released later this month
Output:
the upgraded claude sonnet is now available for all users developers can build with the computer use beta<br>on the anthropic api amazon bedrock and google cloud’s vertex ai<br>the new claude haiku will be released later this month

""".strip()
    return split_prompt