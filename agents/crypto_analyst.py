import openai

class Agent:
    def __init__(self, name, system_prompt, tools=None, memory=None, model="gpt-4"):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.memory = memory or []
        self.model = model

    def run(self, user_input):
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add memory
        for msg in self.memory:
            messages.append(msg)
        messages.append({"role": "user", "content": user_input})

        # Call model
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        reply = response.choices[0].message.content

        # Update memory
        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": reply})
        self.memory = self.memory[-10:]

        return reply

    def add_tool(self, tool_func):
        self.tools.append(tool_func)

    def use_tool(self, name, *args, **kwargs):
        for tool in self.tools:
            if tool.__name__ == name:
                return tool(*args, **kwargs)
        raise ValueError(f"Tool '{name}' not found")
