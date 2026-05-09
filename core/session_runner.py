import os
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule

from agents.market_analyst import MarketAnalyst
from agents.tech_architect import TechArchitect
from agents.devils_advocate import DevilsAdvocate
from agents.business_strategist import BusinessStrategist
from core.models import Session

AGENT_COLORS = {
    "Market Analyst": "cyan",
    "Tech Architect": "green",
    "Devil's Advocate": "red",
    "Business Strategist": "yellow",
}

ROUND_INSTRUCTIONS = {
    1: "This is the opening round. React to the topic directly — share your initial read.",
    2: "Build on what the others have said. Agree, challenge, or add a dimension they missed.",
    3: "Final round. Synthesize the discussion and give your clearest recommendation or verdict.",
}


def run_session(topic: str, rounds: int, save: bool):
    console = Console()
    client = Anthropic()

    agents = [
        MarketAnalyst(client),
        TechArchitect(client),
        DevilsAdvocate(client),
        BusinessStrategist(client),
    ]

    session = Session(topic=topic, rounds=rounds)

    console.print(Rule(f"[bold]Brainstorm: {topic}[/bold]"))
    console.print(f"[dim]{len(agents)} agents · {rounds} rounds[/dim]\n")

    session.add("Facilitator", "user", f"Topic for today's brainstorm: {topic}")

    for round_num in range(1, rounds + 1):
        console.print(Rule(f"[bold dim]Round {round_num}[/bold dim]"))
        instruction = ROUND_INSTRUCTIONS.get(round_num, "Continue the discussion.")

        for agent in agents:
            color = AGENT_COLORS.get(agent.name, "white")
            console.print(f"\n[bold {color}]{agent.name}[/bold {color}] [dim]thinking...[/dim]")

            reply = agent.respond(session, extra_instruction=instruction)
            session.add(agent.name, "assistant", reply)

            console.print(Panel(
                Markdown(reply),
                title=f"[bold {color}]{agent.name}[/bold {color}]",
                border_style=color,
                padding=(1, 2),
            ))

        # Feed the round's output back as user context for next round
        if round_num < rounds:
            round_summary = "\n\n".join(
                f"[{m.agent_name}]: {m.content}"
                for m in session.messages
                if m.role == "assistant"
            )
            session.add("Facilitator", "user", f"Round {round_num} complete. Responses so far:\n\n{round_summary}")

    console.print(Rule("[bold]Session Complete[/bold]"))

    if save:
        _save_session(session, console)


def _save_session(session: Session, console: Console):
    output_dir = Path("output/sessions")
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = session.topic.lower().replace(" ", "_")[:40]
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{slug}.md"
    path = output_dir / filename
    path.write_text(session.transcript(), encoding="utf-8")
    console.print(f"\n[dim]Session saved → {path}[/dim]")
