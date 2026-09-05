"""Quesen CrewAI integration — Agent Firewall + A2A risk tools + enforcement.

v0.4.0 adds the fail-closed enforcement decorator `quesen_guard` and fixes the
`BaseTool` import for modern CrewAI (moved to `crewai.tools`).
"""

from .tool import (
    QuesenFirewallTool,
    QuesenReportTool,
    QuesenSimulateTool,
    QuesenValidateTool,
)
from .guard import quesen_guard

__version__ = "0.5.0"

__all__ = [
    "__version__",
    "QuesenFirewallTool",
    "QuesenValidateTool",
    "QuesenSimulateTool",
    "QuesenReportTool",
    "quesen_guard",
]
