# Cyber and Data Security Architecture (v2 Enhanced)

## Design Principles
- **Zero Trust**: authenticate and authorize every request; assume breach.
- **Least Privilege**: minimal permissions; paper-trading scopes only.
- **Defense in Depth**: multiple overlapping controls.
- **Encryption**: TLS 1.3+ in transit; AES-256 (or equivalent) at rest for any local state.
- **Auditability**: structured logs, immutable multi-hash sealed audit trail.
- **Data Minimization**: only public market data and synthetic fixtures; no PII, no user funds data.

## Controls
| Layer | Control | Implementation Notes |
|-------|---------|----------------------|
| Secrets | Env vars + optional Vault | Never commit; CI gitleaks-style gate |
| API | Key rotation, IP allow-list, request signing | Read-only public endpoints preferred |
| Ingestion | Schema validation, rate-limit handling, redaction, anomaly flags | Reject unexpected fields; apply `redact_sensitive` |
| Processing | Input sanitization, no eval/exec of external data | Pure strategy functions |
| Storage | Encrypted local files / DB; short retention | Multi-hash seals on records |
| Monitoring | Anomaly detection proxies (entropy, isolation-style, residual) | Alert on outliers |
| CI/CD | Secret scan style, dependency audit, license allow-list, lint, coverage | See `.github/workflows/ci.yml` |
| Agent | AGENTS.md rules + PDPA-like guard on fixtures | No personal data in prompts |
| Attestation | Continuous verification proxies + source stamps | `continuous_attestation_proxy` |

## Expanded Redaction
Patterns cover BTC/ETH address-like strings, high-entropy tokens, API key/secret phrases, base64-like blobs, and exchange-specific formats. Applied before logging or sealing.

## Multi-Hash Seals
SHA-256 + SHA3-256 + BLAKE2b for lineage and tamper evidence on signals, risk decisions, and audit events.

## Threat Model (selected)
- API key compromise → mitigated by least privilege + rotation + monitoring
- Data poisoning of signals → validation + multi-source confirmation + anomaly gates
- Insider / agent misuse → human review gate + audit logs + seals
- Exchange outage / rate limits → graceful degradation, circuit breakers
- Secret leakage in prompts → AGENTS.md + redaction + CI tripwire

## Runbooks
Documented in code comments. All changes require human review before merge. Research only; no live execution.
