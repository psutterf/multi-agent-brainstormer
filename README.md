# Multi-Agent Brainstormer

A CLI tool that runs structured brainstorming sessions with four AI agents — each with a distinct persona and expertise — debating and developing ideas together.

## Agents

| Agent | Role |
|---|---|
| **Market Analyst** | Market size, competition, customer pain, timing |
| **Tech Architect** | Feasibility, MVP scope, technical risk |
| **Devil's Advocate** | Failure modes, blind spots, worst-case scenarios |
| **Business Strategist** | Business model, GTM, pricing, moats |

## Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/psutterf/multi-agent-brainstormer.git
cd multi-agent-brainstormer

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Anthropic API key
cp .env.example .env
# Edit .env and paste your key
```

## Usage

```bash
# Basic brainstorm (2 rounds)
python main.py "AI-powered legal document review for small businesses"

# 3 rounds, no save
python main.py "B2B expense management for freelancers" --rounds 3 --no-save

# Quick single round
python main.py "Subscription analytics dashboard" --rounds 1
```

Sessions are saved to `output/sessions/` as markdown files.

## Project Structure

```
multi-agent-brainstormer/
├── agents/
│   ├── base.py               # BaseAgent class
│   ├── market_analyst.py
│   ├── tech_architect.py
│   ├── devils_advocate.py
│   └── business_strategist.py
├── core/
│   ├── models.py             # Session and Message dataclasses
│   └── session_runner.py     # Orchestration logic
├── output/sessions/          # Saved transcripts
├── main.py                   # CLI entry point
└── requirements.txt
```
