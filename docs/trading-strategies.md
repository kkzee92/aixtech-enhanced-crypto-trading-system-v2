# Enhanced Trading Strategies by Asset Class (v2)

All strategies produce research signals only for backtesting and paper simulation. Past performance of any proxy does not indicate future results. Adaptive multi-factor rules incorporate trend, volume, funding, on-chain proxies, relative strength, anomaly scores, and regime filters.

## Majors (BTC, ETH)
**Adaptive multi-factor trend + regime:**
- 50/200 EMA + ATR buffer for primary trend
- Volume confirmation (> 1.4× average)
- Funding rate & OI change filters (avoid crowded positions)
- Mean-reversion overlay on Bollinger extremes
- Stress regime halt; vol-scaled sizing

## Large-Cap Alts (SOL, BNB, ADA, etc.)
- Relative strength vs BTC (price ratio momentum)
- Volume breakout
- Correlation filter: skip or reduce when BTC correlation > 0.85
- Time-stop and anomaly overlay

## DeFi Tokens (UNI, AAVE, LINK, etc.)
- Price action + protocol health proxies (TVL change)
- Anomaly and isolation checks
- Risk-parity style sizing considerations

## Stablecoins
- Peg deviation monitoring (> 40 bps + volume → ALERT)
- No position sizing; alert-only

## High-Volatility / Speculative (memecoins, new listings)
- Maximum 0.5% risk
- Anomaly filter: skip sudden volume spikes without structure
- Hard time stops (handled in risk layer)

## L2 (ARB, OP, etc.)
- Relative strength vs benchmark
- Adaptive multi-timeframe confirmation
- Correlation and cluster awareness

## RWA (tokenized real-world assets)
- Slow multi-scale momentum
- Gap / anomaly halt
- Conservative risk cap

## Perpetuals
- Negative funding carry signals
- Contained drift + OI confirmation
- Anomaly residual filter

## AI-tokens (FET, AGIX, etc.)
- Hybrid burst detection + volume
- Activity proxy and divergence awareness
- Strict horizon and anomaly gate

## Common Enhancements (v2)
- Adaptive position sizing (volatility targeting + anomaly/correlation penalties)
- Portfolio-level correlation risk check
- Explicit regime and anomaly detection proxies
- Multi-hash sealed audit trail
- Offline synthetic demo

All strategies implement `BaseStrategy.generate_signal` and are registered in the strategy map.
