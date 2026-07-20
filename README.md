# Meme Scanner

> A local Solana meme-token risk scanner that explains why a candidate is **blocked**, **watched**, or **passes** configured gates. It is an experimental research tool, not financial advice or a profit system.

Meme Scanner is built for one question: before an operator considers a volatile token, can the system show its safety evidence and stop clearly risky candidates early? The dashboard is local by default and the first-run experience uses deterministic replay data, not a wallet or external API.

## Start safely: Replay Mode

Replay Mode is the default. It has no network requests, no API keys, no wallet access, no transaction signing, and no broadcast capability.

```bash
git clone https://github.com/FeeeeelixWong/meme-scanner.git
cd meme-scanner

python3 scripts/extract_scan_live.py meme_scanner.md --output scan_live.py
MEME_SCANNER_MODE=replay python3 scan_live.py
```

Open [http://localhost:3241](http://localhost:3241). The built-in scenario shows four different policy outcomes:

- `BLOCK`: LP data cannot be verified under strict policy, or a sell cascade is detected.
- `WATCH`: the candidate passes basic checks but is too young or lacks enough confidence for an execution path.
- `PASS`: the configured gates pass. Replay Mode still cannot quote, sign, or trade.

Click any Event Ledger row to inspect the decision summary and the specific rule evidence behind it.

## Runtime Modes

| Mode | What it does | Credentials | Can sign or trade? |
| --- | --- | --- | --- |
| `replay` | Loads deterministic demo fixtures. This is the default. | None | No |
| `observe` | Queries configured market data and creates local observations. | OKX read credentials | No |
| `live` | Experimental transaction path after all entry gates pass. | API credentials and a dedicated wallet | Only with a second explicit gate |

For observation mode, copy `.env.example` to `.env`, add only the API credentials required for market data, then run:

```bash
set -a && source .env && set +a
MEME_SCANNER_MODE=observe python3 scan_live.py
```

`MEME_SCANNER_MODE=live` is intentionally harder to activate: it also requires `ENABLE_LIVE_TRADING=1` and a wallet key. Live execution is experimental, is not required for the project demo, and is outside the safe default path. Never use a primary wallet, disclose a private key, or expose the dashboard to the public internet.

## What the scanner explains

The dashboard separates discovery from permission to act:

1. **Discovery filters** reject unsuitable market-cap, age, holder, developer-holding, and volume profiles.
2. **Risk gates** fail closed on missing LP evidence and reject excessive bundle concentration, developer rug history, developer concentration, or suspicious wallet patterns.
3. **Market-pressure checks** flag sell streaks, concentrated sell pressure, recent crashes, anti-chase conditions, and wash-like activity.
4. **Execution-quality gates** can keep a visible signal in `WATCH` even when it is not eligible for an execution path.

This is deliberately a risk-first workflow. A `PASS` means only that the configured checks did not block the candidate at that moment; it does not predict performance, safety, liquidity, or profitability.

## Local Dashboard

The dashboard binds to `127.0.0.1:3241` by default and provides:

- Event Ledger with copyable contract addresses and click-through decision evidence.
- Signal Queue distinguishing `WATCH` from eligible candidates.
- Risk Blocks, positions, trade-history, and session summaries.
- A read-only TraderSoul reflection rail. It does not override the deterministic safety gates.

## Validate the project

```bash
python3 -m unittest discover -s tests -v
python3 scripts/extract_scan_live.py meme_scanner.md --output /tmp/scan_live.py
python3 -m py_compile /tmp/scan_live.py
```

The checked-in source of truth is [`meme_scanner.md`](./meme_scanner.md). `scan_live.py` is generated locally and intentionally ignored so the skill file and extraction test remain the single reviewed implementation.

## Safety Notes

- This project is for research and demonstration. Meme-token markets can result in a total loss.
- Do not treat scanner output as financial, legal, or investment advice.
- No external data check can guarantee that a token is safe or that a transaction will succeed.
- Keep credentials local and use a dedicated, low-value wallet only if independently choosing to explore the experimental live path.

## License

[MIT](./LICENSE)
