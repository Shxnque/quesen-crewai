"""
Fail-closed enforcement decorator for CrewAI.

v0.4.0 tracks quesen-sdk 0.5.0. Identical contract to the LangChain integration:
``quesen_guard`` wraps ``quesen_sdk.QuesenFirewall.guard`` so any Python callable
executes ONLY when Quesen returns PASS for the described action; otherwise the
body never runs and ``quesen_sdk.tsc.TscBlocked`` is raised (fail-closed). The
verdict is attached to the wrapped callable as ``.last_decision``.

Example::

    from quesen_crewai import quesen_guard

    @quesen_guard(base_url="https://<engine>", sandbox=True,
                  action="send_data", data_class="secret")
    def post_to_pastebin(text: str) -> str:
        ...  # only runs on PASS

Doctrine anchors: §2 Determinism preserved; fail-closed.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from quesen_sdk import QuesenClient, QuesenFirewall
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-crewai requires `quesen-sdk>=0.5.0`. Install with `pip install quesen-crewai`."
    ) from exc

__all__ = ["quesen_guard"]


def quesen_guard(
    *,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    sandbox: bool = False,
    client: Optional[QuesenClient] = None,
    firewall: Optional[QuesenFirewall] = None,
    timeout: float = 5.0,
    retries: int = 2,
    **action: Any,
):
    """Return a fail-closed enforcement decorator bound to a Quesen firewall.

    ``**action`` describes the high-risk action and is forwarded verbatim to
    :meth:`quesen_sdk.QuesenFirewall.check`.
    """
    fw = firewall
    if fw is None:
        if client is not None:
            fw = QuesenFirewall(client=client)
        elif sandbox and not api_key:
            fw = QuesenFirewall.sandbox(base_url, timeout=timeout, retries=retries)
        else:
            fw = QuesenFirewall(
                base_url=base_url, api_key=api_key, timeout=timeout, retries=retries
            )
    return fw.guard(**action)
