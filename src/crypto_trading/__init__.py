"""AIxTech enhanced crypto trading information system v2 (paper/research only)."""
__version__ = "2.0.0"
from .strategies import get_strategy, STRATEGIES
from .risk import compute_position_size, risk_gate
from .security import redact_sensitive, multi_hash_seal
