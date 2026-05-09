from anthropic import Anthropic
from core.models import Session


class BaseAgent:
    name: str = "Agent"
    system_prompt: str = ""

    def __init__(self, client: Anthropic):
        self.client = client

    def respond(self, session: Session, extra_instruction: str = "") -> str:
        history = self._build_history(session)
        system = self.system_prompt
        if extra_instruction:
            system += f"\n\n{extra_instruction}"

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system,
            messages=history,
        )
        return response.content[0].text

    def _build_history(self, session: Session) -> list:
        """Convert session messages into Anthropic message format."""
        history = []
        for msg in session.messages:
            if msg.role == "user":
                history.append({"role": "user", "content": msg.content})
            elif msg.role == "assistant":
                history.append({
                    "role": "user",
                    "content": f"[{msg.agent_name}]: {msg.content}"
                })
        # Anthropic requires messages to alternate; collapse consecutive same-role messages
        merged = []
        for msg in history:
            if merged and merged[-1]["role"] == msg["role"]:
                merged[-1]["content"] += "\n\n" + msg["content"]
            else:
                merged.append(dict(msg))
        return merged
