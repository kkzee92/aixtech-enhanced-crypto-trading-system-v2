"""Tests for strategies and risk (synthetic data only)."""
import pytest
from src.crypto_trading.strategies import get_strategy
from src.crypto_trading.risk import compute_position_size, risk_gate
from src.crypto_trading.security import redact_sensitive, multi_hash_seal

def test_majors_buy():
    strat = get_strategy("majors")
    data = {"price": 65000, "ema_50": 64000, "ema_200": 62000, "atr": 1000, "volume_ratio": 1.6, "funding_rate": 0.0001, "oi_change_pct": 0.01, "regime": "trend"}
    assert strat.generate_signal(data) == "BUY"

def test_risk_size_positive():
    data = {"realized_vol": 0.4, "anomaly_score": 0.1, "btc_correlation": 0.6}
    size = compute_position_size("BUY", "majors", data)
    assert 0 < size <= 0.08

def test_risk_gate_anomaly():
    data = {"anomaly_score": 0.8}
    assert risk_gate("BUY", "majors", data) == "HOLD"

def test_redaction():
    text = "api_key=sk-1234567890abcdef"
    assert "[REDACTED]" in redact_sensitive(text)

def test_multi_hash():
    seal = multi_hash_seal("test")
    assert len(seal["sha256"]) == 64
    assert "blake2b" in seal
