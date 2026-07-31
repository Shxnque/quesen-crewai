# Quesen — CrewAI Tool

> Deterministic A2A risk validation as a CrewAI `BaseTool`. Drop it on any Agent, any Crew.

**Status:** v0.2.0 · tracks Quesen engine v1.10.0 · receipt provenance forwarded.
**Developer portal:** https://senueren.co.za/quesen · **Source:** https://github.com/Shxnque/quesen

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

## Receipt provenance (v1.10)

Calling `QuesenValidateTool._run(...)` returns the raw response dict from the
underlying `quesen-sdk` client. Against a v1.10.0+ engine that dict includes:

- `input_snapshot_hash` — SHA-256 over canonical request JSON.
- `commit_sha` — git SHA of the ruleset live at decision time (or `"unknown"`).

Both flow through untouched for CrewAI callers to log or verify. See the
[public API reference](https://github.com/Shxnque/quesen/blob/main/docs/api-reference.md#receipt-provenance-v110)
for the contract.

## Tools shipped

- `QuesenValidateTool` — wraps `/validate`
- `QuesenSimulateTool` — wraps `/simulate`
- `QuesenReportTool`   — wraps `/report` (v1.1 schema)

MIT license. See [`senueren.co.za/quesen`](https://senueren.co.za/quesen) for canonical documentation.
