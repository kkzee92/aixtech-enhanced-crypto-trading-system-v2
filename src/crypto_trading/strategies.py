"""Enhanced multi-factor adaptive strategies per asset class (research/paper only)."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import math

class BaseStrategy(ABC):
    """Abstract base for all strategies."""
    name: str = "base"

    @abstractmethod
    def generate_signal(self, data: Dict[str, Any]) -> str:
        """Return 'BUY', 'SELL', 'HOLD', or 'ALERT'. Pure and side-effect free."""
        raise NotImplementedError

    def _safe_get(self, data: Dict[str, Any], key: str, default: float = 0.0) -> float:
        try:
            val = float(data.get(key, default))
            return val if math.isfinite(val) else default
        except (TypeError, ValueError):
            return default

class MajorsStrategy(BaseStrategy):
    """Adaptive multi-factor for BTC/ETH majors."""
    name = "majors"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        price = self._safe_get(data, "price")
        ema50 = self._safe_get(data, "ema_50", price)
        ema200 = self._safe_get(data, "ema_200", price)
        atr = self._safe_get(data, "atr", price * 0.02)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        funding = self._safe_get(data, "funding_rate", 0.0)
        oi_change = self._safe_get(data, "oi_change_pct", 0.0)
        regime = data.get("regime", "trend")

        if regime == "stress":
            return "HOLD"
        # Trend + volume + funding filter
        if ema50 > ema200 and price > ema50 + atr * 0.5 and volume_ratio > 1.4 and funding < 0.0008 and oi_change > -0.05:
            return "BUY"
        if ema50 < ema200 and price < ema50 - atr * 0.5 and volume_ratio > 1.4 and funding > -0.0008:
            return "SELL"
        # Mean-reversion overlay
        bb_upper = self._safe_get(data, "bb_upper", price * 1.025)
        bb_lower = self._safe_get(data, "bb_lower", price * 0.975)
        if price >= bb_upper and volume_ratio > 1.2:
            return "SELL"
        if price <= bb_lower and volume_ratio > 1.2:
            return "BUY"
        return "HOLD"

class LargeAltsStrategy(BaseStrategy):
    """Relative strength + breakout for large alts."""
    name = "large_alts"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        btc_ratio_mom = self._safe_get(data, "btc_ratio_momentum", 0.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        corr = self._safe_get(data, "btc_correlation", 0.5)
        if corr > 0.85:
            return "HOLD"  # reduce exposure under high correlation
        if btc_ratio_mom > 0.015 and volume_ratio > 1.7:
            return "BUY"
        if btc_ratio_mom < -0.015 and volume_ratio > 1.5:
            return "SELL"
        return "HOLD"

class DeFiStrategy(BaseStrategy):
    """Price + protocol health proxies with isolation check."""
    name = "defi"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        price_change = self._safe_get(data, "price_change_pct", 0.0)
        tvl_change = self._safe_get(data, "tvl_change_pct", 0.0)
        anomaly = self._safe_get(data, "anomaly_score", 0.0)
        if anomaly > 0.7:
            return "HOLD"
        if price_change > 0.008 and tvl_change > 0.004:
            return "BUY"
        if price_change < -0.025 or tvl_change < -0.015:
            return "SELL"
        return "HOLD"

class StableStrategy(BaseStrategy):
    """Peg monitoring with volume confirmation."""
    name = "stables"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        deviation = abs(self._safe_get(data, "peg_deviation_bps", 0.0))
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        if deviation > 40 and volume_ratio > 1.3:
            return "ALERT"
        return "HOLD"

class HighVolStrategy(BaseStrategy):
    """Strict controls for speculative assets."""
    name = "high_vol"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        price_change = self._safe_get(data, "price_change_pct", 0.0)
        anomaly = self._safe_get(data, "anomaly_score", 0.0)
        if anomaly > 0.5 or (volume_ratio > 2.5 and abs(price_change) > 0.04):
            return "HOLD"  # skip anomalous bursts
        return "HOLD"

class L2Strategy(BaseStrategy):
    """Relative strength vs benchmark for L2s."""
    name = "l2"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        rel_strength = self._safe_get(data, "relative_strength", 0.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        if rel_strength > 0.02 and volume_ratio > 1.6:
            return "BUY"
        if rel_strength < -0.02 and volume_ratio > 1.4:
            return "SELL"
        return "HOLD"

class RWAStrategy(BaseStrategy):
    """Slow multi-scale for real-world asset tokens."""
    name = "rwa"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        price_change = self._safe_get(data, "price_change_pct", 0.0)
        anomaly = self._safe_get(data, "anomaly_score", 0.0)
        if anomaly > 0.6 or abs(price_change) > 0.05:
            return "HOLD"
        if price_change > 0.005:
            return "BUY"
        if price_change < -0.008:
            return "SELL"
        return "HOLD"

class PerpetualStrategy(BaseStrategy):
    """Funding carry + contained drift."""
    name = "perpetual"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        funding = self._safe_get(data, "funding_rate", 0.0)
        oi_change = self._safe_get(data, "oi_change_pct", 0.0)
        anomaly = self._safe_get(data, "anomaly_score", 0.0)
        if anomaly > 0.6:
            return "HOLD"
        if funding < -0.0003 and oi_change > 0:
            return "BUY"  # negative funding carry
        if funding > 0.0005:
            return "SELL"
        return "HOLD"

class AITokenStrategy(BaseStrategy):
    """Hybrid burst + activity for AI tokens."""
    name = "ai_token"

    def generate_signal(self, data: Dict[str, Any]) -> str:
        price_change = self._safe_get(data, "price_change_pct", 0.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        anomaly = self._safe_get(data, "anomaly_score", 0.0)
        if anomaly > 0.55:
            return "HOLD"
        if price_change > 0.03 and volume_ratio > 2.0:
            return "BUY"
        if price_change < -0.04:
            return "SELL"
        return "HOLD"

# Registry
STRATEGIES: Dict[str, BaseStrategy] = {
    "majors": MajorsStrategy(),
    "large_alts": LargeAltsStrategy(),
    "defi": DeFiStrategy(),
    "stables": StableStrategy(),
    "high_vol": HighVolStrategy(),
    "l2": L2Strategy(),
    "rwa": RWAStrategy(),
    "perpetual": PerpetualStrategy(),
    "ai_token": AITokenStrategy(),
}

def get_strategy(asset_class: str) -> Optional[BaseStrategy]:
    return STRATEGIES.get(asset_class.lower())
