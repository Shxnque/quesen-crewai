"""
CrewAI BaseTool wrappers around the Quesen Python SDK.

CrewAI's tool contract is a Pydantic v2 model class-attribute (`args_schema`)
plus a `_run(**kwargs)` method — same shape as LangChain, but the base class
comes from `crewai_tools`.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Type

try:
    from crewai_tools import BaseTool
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-crewai requires `crewai-tools` and `pydantic`. "
        "Install with `pip install quesen-crewai`."
    ) from exc

try:
    from quesen_sdk import QuesenClient
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-crewai requires `quesen-sdk`. Install with `pip install quesen-sdk`."
    ) from exc


class _ValidateInput(BaseModel):
    domain_age_days: Optional[int] = Field(default=None, ge=0)
    engagement_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    scam_keyword_count: Optional[int] = Field(default=None, ge=0)
    client_request_id: Optional[str] = Field(default=None, max_length=128)


class _SimulateInput(BaseModel):
    domain_age_days: Optional[int] = Field(default=None, ge=0)
    engagement_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    scam_keyword_count: Optional[int] = Field(default=None, ge=0)
    weights_override: Optional[Dict[str, float]] = None
    thresholds_override: Optional[Dict[str, float]] = None


class _ReportInput(BaseModel):
    request_id: str = Field(min_length=1, max_length=128)
    outcome: str = Field(description="RUG | LOSS | OK | WIN | UNKNOWN")
    notes: Optional[str] = Field(default=None, max_length=1000)
    realized_pnl: Optional[float] = None
    elapsed_seconds: Optional[int] = Field(default=None, ge=0)
    venue: Optional[str] = Field(default=None, max_length=64)
    signal_hash: Optional[str] = Field(default=None, max_length=128)


class _BaseQuesenTool(BaseTool):
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    timeout: float = 5.0
    retries: int = 2
    _client: Optional[QuesenClient] = None

    def _get_client(self) -> QuesenClient:
        if self._client is None:
            self._client = QuesenClient(
                base_url=self.base_url, api_key=self.api_key,
                timeout=self.timeout, retries=self.retries,
            )
        return self._client


class QuesenValidateTool(_BaseQuesenTool):
    name: str = "quesen_validate"
    description: str = (
        "Deterministic A2A risk validation. Call BEFORE taking any high-consequence "
        "action. Returns PROCEED / REVIEW / SKIP with risk_score, confidence, and "
        "named conflict_triggers."
    )
    args_schema: Type[BaseModel] = _ValidateInput

    def _run(self, **kwargs: Any) -> Dict[str, Any]:
        r = self._get_client().validate(
            domain_age_days=kwargs.get("domain_age_days"),
            engagement_ratio=kwargs.get("engagement_ratio"),
            scam_keyword_count=kwargs.get("scam_keyword_count"),
            client_request_id=kwargs.get("client_request_id"),
        )
        return r.raw


class QuesenSimulateTool(_BaseQuesenTool):
    name: str = "quesen_simulate"
    description: str = (
        "Free counterfactual scoring — not charged. Test how the risk model "
        "responds to alternate weights or thresholds."
    )
    args_schema: Type[BaseModel] = _SimulateInput

    def _run(self, **kwargs: Any) -> Dict[str, Any]:
        r = self._get_client().simulate(
            domain_age_days=kwargs.get("domain_age_days"),
            engagement_ratio=kwargs.get("engagement_ratio"),
            scam_keyword_count=kwargs.get("scam_keyword_count"),
            weights_override=kwargs.get("weights_override"),
            thresholds_override=kwargs.get("thresholds_override"),
        )
        return r.raw


class QuesenReportTool(_BaseQuesenTool):
    name: str = "quesen_report"
    description: str = (
        "Report the realized outcome of a decision back to Quesen. Pass the "
        "request_id from /validate plus an outcome enum "
        "(RUG|LOSS|OK|WIN|UNKNOWN)."
    )
    args_schema: Type[BaseModel] = _ReportInput

    def _run(self, **kwargs: Any) -> Dict[str, Any]:
        r = self._get_client().report(
            request_id=kwargs["request_id"],
            outcome=kwargs["outcome"],
            notes=kwargs.get("notes"),
            realized_pnl=kwargs.get("realized_pnl"),
            elapsed_seconds=kwargs.get("elapsed_seconds"),
            venue=kwargs.get("venue"),
            signal_hash=kwargs.get("signal_hash"),
        )
        return r.raw
