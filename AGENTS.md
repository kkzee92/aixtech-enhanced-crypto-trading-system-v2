# AGENTS.md — Rules for AI coding agents

This repository demonstrates a secure AI-agent harness for developing automated cryptocurrency trading *information* systems.

## Absolute rules
- Never commit secrets, API keys, private keys, seeds, or personal data.
- Use only synthetic fixtures or public market data. No production data in prompts or code.
- All strategy outputs are research signals for paper simulation only. Never implement live order execution or withdrawal logic.
- Human review is required before any merge (Definition of Done = CI green + human approval).
- Prefer pure functions, type hints, and comprehensive tests.
- Run local CI gates (`scripts/ci_local.sh` style) before proposing changes.

## Preferred practices
- Extend `BaseStrategy` for new asset classes.
- Keep risk caps and anomaly gates in `risk.py`.
- Use `security.py` helpers for redaction and seals.
- Document enhancements in `docs/`.
- Add AI-disclosure trailers to commits when assisted: `AI-Assisted: yes`.

Inspired by [zeekiankok92/aixtech-agent-harness-demo](https://github.com/zeekiankok92/aixtech-agent-harness-demo).
