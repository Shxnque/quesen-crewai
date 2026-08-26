# Changelog

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
