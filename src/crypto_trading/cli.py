"""CLI for the enhanced crypto trading information system (paper only)."""
import argparse
import json
from typing import Dict, Any

from .strategies import get_strategy
from .risk import compute_position_size, risk_gate
from .security import redact_sensitive, multi_hash_seal, anomaly_score

def demo_run() -> None:
    """Run a synthetic demo across asset classes."""
    synthetic_cases = [
        {"asset_class": "majors", "data": {"price": 65000, "ema_50": 64000, "ema_200": 62000, "atr": 1200, "volume_ratio": 1.6, "funding_rate": 0.0002, "oi_change_pct": 0.02, "regime": "trend", "realized_vol": 0.4, "anomaly_score": 0.1, "btc_correlation": 1.0}},
        {"asset_class": "large_alts", "data": {"btc_ratio_momentum": 0.025, "volume_ratio": 1.9, "btc_correlation": 0.65, "realized_vol": 0.6, "anomaly_score": 0.2}},
        {"asset_class": "defi", "data": {"price_change_pct": 0.012, "tvl_change_pct": 0.006, "anomaly_score": 0.15, "realized_vol": 0.7}},
        {"asset_class": "stables", "data": {"peg_deviation_bps": 55, "volume_ratio": 1.4}},
        {"asset_class": "high_vol", "data": {"volume_ratio": 1.2, "price_change_pct": 0.01, "anomaly_score": 0.3}},
        {"asset_class": "l2", "data": {"relative_strength": 0.03, "volume_ratio": 1.8, "realized_vol": 0.5}},
        {"asset_class": "perpetual", "data": {"funding_rate": -0.0004, "oi_change_pct": 0.01, "anomaly_score": 0.1}},
        {"asset_class": "ai_token", "data": {"price_change_pct": 0.04, "volume_ratio": 2.2, "anomaly_score": 0.25}},
    ]
    print("=== AIxTech Enhanced Crypto Trading Info System v2 - Synthetic Demo ===\n")
    for case in synthetic_cases:
        cls = case["asset_class"]
        data = case["data"]
        strategy = get_strategy(cls)
        if not strategy:
            continue
        raw_signal = strategy.generate_signal(data)
        gated = risk_gate(raw_signal, cls, data)
        size = compute_position_size(gated, cls, data)
        seal = multi_hash_seal(json.dumps({"class": cls, "signal": gated, "size": size}))
        print(f"{cls.upper():12} | signal: {gated:6} | size: {size:.4f} | seal: {seal['sha256'][:12]}...")
    print("\nAll outputs are research signals on synthetic data. No live execution.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Crypto trading information system (paper only)")
    parser.add_argument("command", choices=["demo"], help="Command to run")
    args = parser.parse_args()
    if args.command == "demo":
        demo_run()

if __name__ == "__main__":
    main()
