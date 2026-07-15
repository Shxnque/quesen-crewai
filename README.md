# Quesen — CrewAI Tool

> Deterministic A2A risk validation as a CrewAI `BaseTool`. Drop it on any Agent, any Crew.

**Parent repo:** https://github.com/Shxnque/Quesen-sib

---

## Install

```bash
pip install quesen-crewai
# or:
pip install git+https://github.com/Shxnque/quesen-crewai.git
```

## 30-second usage

```python
from crewai import Agent, Task, Crew
from quesen_crewai import QuesenValidateTool, QuesenReportTool

defender = Agent(
    role="Risk Officer",
    goal="Prevent the trading agent from touching rugpulls.",
    backstory="You block any action that Quesen labels SKIP.",
    tools=[QuesenValidateTool(base_url="https://<your-quesen>", api_key="sk_live_abc")],
)

check = Task(
    description="Validate this opportunity: domain_age_days=1, engagement_ratio=0.95, scam_keyword_count=4",
    agent=defender,
    expected_output="A PROCEED / REVIEW / SKIP decision with risk_score and conflict_triggers.",
)

crew = Crew(agents=[defender], tasks=[check])
print(crew.kickoff())
```

## Tools shipped

- `QuesenValidateTool` — wraps `/validate`
- `QuesenSimulateTool` — wraps `/simulate`
- `QuesenReportTool`   — wraps `/report` (v1.1 schema)

MIT license. Extracted from `Shxnque/Quesen-sib` `sdks/crewai/`.
