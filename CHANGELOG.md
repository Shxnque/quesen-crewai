# Changelog

## [0.5.0] — 2026-09-05 · SDK 0.6.0 parity · offline verdict replay

### Added
- **`verify_recompute=True`** on `QuesenFirewallTool` — REPLAY the verdict offline
  against the exact context and merge `receipt_recomputed` + `receipt_verification`
  into the tool output (BEA criticism-ledger C-003 / C-004).

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.6.0`.

## [0.4.0] — 2026-09-05 · SDK 0.5.0 parity · enforcement + verifiable receipts

### Added
- **`quesen_guard(...)`** — fail-closed enforcement decorator (wraps
  `quesen_sdk.QuesenFirewall.guard`): a gated callable runs ONLY on PASS,
  otherwise `TscBlocked` is raised. Verdict attached as `.last_decision`.
- **Independent receipt verification** on `QuesenFirewallTool` via
  `verify_receipts=True` (+ optional `engine_public_key_hex`).

### Fixed
- **`BaseTool` import** now resolves against modern CrewAI (`crewai.tools`),
  with a fallback to legacy `crewai_tools`. Previously failed to import on
  crewai/crewai-tools ≥ 1.x.

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.5.0`.

## [0.3.0] — 2026-08-27 · Agent Firewall tool (TSC v2)

### Added
- **`QuesenFirewallTool`** — CrewAI `BaseTool` wrapping the Quesen Agent Firewall
  (`POST /tsc/validate`): deterministic PASS/REVIEW/BLOCK/SKIP + audit receipt
  before a high-risk action. `sandbox=True` self-serves a free key.

### Changed
- Bumped `quesen-sdk` dependency floor to `>=0.4.1`.

## [0.2.0] — 2026-07-31 · Tracks engine v1.10.0 receipt provenance

### Changed
- Bumped `__version__` `0.1.0` → `0.2.0`.
- Bumped `quesen-sdk` dependency floor to `>=0.2.0`.
- README documents that the raw response dict returned by `QuesenValidateTool`
  now carries `input_snapshot_hash` and `commit_sha` against v1.10.0+ engines.

### Notes
- No code change to the tool wrappers. `._run(...)` returns `r.raw`; the two
  new fields flow through automatically from `quesen-sdk` 0.2.0.

## [0.1.0] — 2026-07-16 · Initial release
- Three CrewAI `BaseTool` subclasses.

[0.2.0]: https://github.com/Shxnque/quesen-crewai/releases/tag/v0.2.0
[0.1.0]: https://github.com/Shxnque/quesen-crewai/releases/tag/v0.1.0
