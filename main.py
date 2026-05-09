import os
import click
from dotenv import load_dotenv

load_dotenv()


@click.command()
@click.argument("topic")
@click.option("--rounds", "-r", default=2, show_default=True, help="Number of discussion rounds (1-3)")
@click.option("--save/--no-save", default=True, show_default=True, help="Save session transcript to output/sessions/")
def brainstorm(topic: str, rounds: int, save: bool):
    """Run a multi-agent brainstorming session on TOPIC.

    Example:\n
        python main.py "AI-powered legal document review for small businesses" --rounds 2
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise click.ClickException("ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")

    if not 1 <= rounds <= 3:
        raise click.ClickException("Rounds must be between 1 and 3.")

    from core.session_runner import run_session
    run_session(topic=topic, rounds=rounds, save=save)


if __name__ == "__main__":
    brainstorm()
