# hyperliquid_adapter

## Path
- `C:\laragon\www\hyperliquid_adapter`

## Purpose
Safe adapter for Hyperliquid market-data monitoring and guarded trading execution.

## Current state
- Initial scaffold completed and committed: `6372cda Initial Hyperliquid adapter scaffold`
- Python package with CLI, read-only `/info` client, guarded SDK exchange wrapper, local risk checks, tests, README, and safety docs.

## Safety rules
- Default network is testnet.
- Read-only functions do not require keys.
- Signed trading actions require `HL_SECRET_KEY` and official `hyperliquid-python-sdk`.
- Mainnet execution requires all gates: `--execute`, `HL_LIVE_TRADING_ENABLED=true`, configured `HL_APPROVAL_TOKEN`, matching CLI `--approval-token`, and local risk checks.
- Clio must still get explicit Afu approval before any live Hyperliquid order.
- No secrets in repo; `.env` is gitignored.

## Useful commands
```powershell
cd C:\laragon\www\hyperliquid_adapter
$env:PYTHONPATH='C:\laragon\www\hyperliquid_adapter\src'
python -m unittest discover -s tests
python -m hyperliquid_adapter.cli mids --network testnet --coins BTC ETH SOL
python -m hyperliquid_adapter.cli validate-order --coin ETH --side buy --size 0.01 --price 2000
```
