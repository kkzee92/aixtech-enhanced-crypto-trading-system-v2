"""Zero-trust security helpers: redaction, multi-hash seals, anomaly proxies (research only)."""
import hashlib
import re
from typing import Dict, Any, List
import math
from collections import Counter

# Expanded redaction patterns (keys, seeds, tokens, high-entropy, exchange formats)
REDACTION_PATTERNS = [
    re.compile(r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"),  # BTC address-like
    re.compile(r"\b0x[a-fA-F0-9]{40}\b"),  # ETH address
    re.compile(r"\b[a-zA-Z0-9]{20,}\b"),  # high entropy / API keys
    re.compile(r"(?i)(api[_-]?key|secret|private[_-]?key|seed|mnemonic|wallet)\s*[:=]\s*\S+"),
    re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b"),  # base64-like
]

def redact_sensitive(text: str) -> str:
    """Apply redaction patterns. Returns sanitized string."""
    for pattern in REDACTION_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text

def multi_hash_seal(data: str) -> Dict[str, str]:
    """Produce multi-hash seal (SHA-256 + SHA3-256 + BLAKE2b proxies)."""
    raw = data.encode("utf-8")
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sha3_256": hashlib.sha3_256(raw).hexdigest(),
        "blake2b": hashlib.blake2b(raw, digest_size=32).hexdigest(),
    }

def entropy_score(text: str) -> float:
    """Simple entropy proxy (0-1). High entropy may indicate secrets or noise."""
    if not text:
        return 0.0
    counts = Counter(text)
    length = len(text)
    entropy = -sum((c / length) * math.log2(c / length) for c in counts.values() if c > 0)
    return min(1.0, entropy / 8.0)  # normalize roughly

def anomaly_score(features: Dict[str, float]) -> float:
    """Isolation-style anomaly proxy based on z-score extremes."""
    scores = []
    for k, v in features.items():
        if "ratio" in k or "change" in k:
            if abs(v) > 3.0:
                scores.append(0.8)
            elif abs(v) > 2.0:
                scores.append(0.5)
    return min(1.0, max(scores) if scores else 0.0)

def continuous_attestation_proxy(event: Dict[str, Any]) -> str:
    """Stub for continuous verification / source attestation."""
    seal = multi_hash_seal(str(sorted(event.items())))
    return f"attested:{seal['sha256'][:16]}"
