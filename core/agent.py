import openai
from typing import List, Callable, Optional, Dict

class Agent:
    def __init__(
        self,
        name: str,
        system_prompt: str,
        tools: Optional[List[Callable]] = None,
        memory: Optional[List[Dict]] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        self.name = name
        self.system_prompt = system_prompt.strip()
        self.tools = tools or []
        self.memory = memory or []
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def build_messages(self, user_input: str) -> List[Dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory[-10:])
        messages.append({"role": "user", "content": user_input})
        return messages

    def run(self, user_input: str) -> str:
        messages = self.build_messages(user_input)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            reply = response.choices[0].message["content"].strip()

            # Update memory
            self.memory.append({"role": "user", "content": user_input})
            self.memory.append({"role": "assistant", "content": reply})
            self.memory = self.memory[-20:]  # limit to last 10 exchanges

            return reply

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def add_tool(self, tool_func: Callable):
        self.tools.append(tool_func)

    def list_tools(self) -> List[str]:
        return [t.__name__ for t in self.tools]

    def use_tool(self, name: str, *args, **kwargs) -> str:
        for tool in self.tools:
            if tool.__name__ == name:
                try:
                    return tool(*args, **kwargs)
                except Exception as e:
                    return f"⚠️ Tool error: {str(e)}"
        return f"❌ Tool '{name}' not found"
