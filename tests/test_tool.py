"""CrewAI wrapper smoke tests — import-only; live tests live in the parent repo SDK suite."""

import pytest

crewai_tools = pytest.importorskip("crewai_tools")
quesen_sdk = pytest.importorskip("quesen_sdk")

from quesen_crewai import QuesenReportTool, QuesenSimulateTool, QuesenValidateTool


def test_tools_import_and_carry_schema():
    for cls in (QuesenValidateTool, QuesenSimulateTool, QuesenReportTool):
        t = cls(base_url="http://x", api_key="k")
        assert t.name.startswith("quesen_")
        assert t.args_schema is not None
