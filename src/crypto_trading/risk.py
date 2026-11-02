"""Adaptive risk engine with class caps, vol-targeting, correlation and anomaly gates (paper only)."""
from typing import Dict, Any

CLASS_RISK_CAPS = {
    "majors": 0.08,
    "large_alts": 0.04,
    "defi": 0.02,
    "stables": 0.0,  # alerts only
    "high_vol": 0.005,
    "l2": 0.03,
    "rwa": 0.02,
    "perpetual": 0.02,
    "ai_token": 0.01,
}

def compute_position_size(signal: str, asset_class: str, data: Dict[str, Any]) -> float:
    """Return suggested risk fraction (0.0 - cap). Adaptive to vol and anomaly."""
    if signal not in ("BUY", "SELL"):
        return 0.0
    base_cap = CLASS_RISK_CAPS.get(asset_class.lower(), 0.01)
    vol = float(data.get("realized_vol", 0.5))
    anomaly = float(data.get("anomaly_score", 0.0))
    corr = float(data.get("btc_correlation", 0.5))
    # Vol targeting: scale down in high vol
    vol_scale = max(0.3, 1.0 - vol)
    # Anomaly and correlation penalties
    anomaly_penalty = 1.0 - min(0.8, anomaly)
    corr_penalty = 1.0 if corr < 0.75 else 0.6
    size = base_cap * vol_scale * anomaly_penalty * corr_penalty
    return max(0.0, min(base_cap, size))

def risk_gate(signal: str, asset_class: str, data: Dict[str, Any]) -> str:
    """Apply multi-gate risk check. May downgrade signal."""
    if data.get("kill_switch", False):
        return "HOLD"
    if float(data.get("drawdown", 0.0)) > 0.15:
        return "HOLD"
    anomaly = float(data.get("anomaly_score", 0.0))
    if anomaly > 0.75:
        return "HOLD"
    return signal
