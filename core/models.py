from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Message:
    agent_name: str
    role: str  # "user" | "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Session:
    topic: str
    rounds: int
    messages: List[Message] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add(self, agent_name: str, role: str, content: str):
        self.messages.append(Message(agent_name=agent_name, role=role, content=content))

    def transcript(self) -> str:
        lines = [f"# Brainstorm Session: {self.topic}", f"Started: {self.started_at}", ""]
        for msg in self.messages:
            if msg.role == "assistant":
                lines.append(f"## {msg.agent_name}")
                lines.append(msg.content)
                lines.append("")
        return "\n".join(lines)
