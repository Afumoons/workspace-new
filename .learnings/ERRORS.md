## [ERR-20260511-001] web_search_dns_failure

**Logged**: 2026-05-11T09:26:00+07:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
`web_search` failed repeatedly with `getaddrinfo ENOTFOUND html.duckduckgo.com` during Morning Market Brief cron.

### Details
Multiple parallel market/news searches failed due DNS resolution for DuckDuckGo HTML endpoint. Workaround used direct `web_fetch` to Stooq, CoinGecko, ForexFactory calendar, and Treasury/MarketWatch where available. Yahoo Finance and Investing.com were rate-limited/blocked.

### Suggested Action
For scheduled market briefs, prefer resilient direct-data fallbacks first (Stooq CSV, CoinGecko, ForexFactory calendar, Treasury/FRED where working), then use web_search only for narrative/news context. Consider configuring a more reliable search provider or fallback endpoint.

### Metadata
- Source: error
- Tags: web_search, dns, market-brief, cron

---
## [ERR-20260514-001] autonomous_trading_ai_daily_audit_path_and_shell_gotchas

**Logged**: 2026-05-14T04:14:00+07:00
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Daily ATA governance audit initially failed on the prompted workspace path and two PowerShell/Python invocation gotchas.

### Error
```
Get-ChildItem: Cannot find path C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai
ModuleNotFoundError: No module named 'autonomous_trading_ai' when running scripts\print_live_summary.py from repo root without PYTHONPATH
PowerShell rejected bash-style heredoc: python - <<'PY'
```

### Context
- Actual known repo path used successfully: C:\laragon\www\autonomous_trading_ai
- Python repo scripts need PYTHONPATH=C:\laragon\www in this environment.
- PowerShell does not support bash heredoc syntax; use temp scripts or PowerShell here-strings.

### Suggested Fix
For future ATA cron runs, prefer the long-term memory path if the prompted path is absent, set PYTHONPATH before package scripts, and avoid bash heredocs in PowerShell.

### Metadata
- Reproducible: yes
- Related Files: C:\laragon\www\autonomous_trading_ai
- Tags: autonomous_trading_ai, powershell, pythonpath, cron

---
## [ERR-20260514-002] market_brief_data_source_failures

**Logged**: 2026-05-14T04:35:00+07:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Morning Market Brief hit recurring `web_search` DNS failure plus blocked/rate-limited market endpoints.

### Error
```
web_search: getaddrinfo ENOTFOUND html.duckduckgo.com
web_fetch Investing.com: 403 / Just a moment
web_fetch ForexFactory: getaddrinfo ENOTFOUND www.forexfactory.com
web_fetch Yahoo chart API: 429 Too Many Requests
```

### Context
Used direct fallbacks that worked: MarketWatch/CNBC pages, Stooq quote CSV one symbol at a time, CoinGecko simple price, and Treasury XML yield curve.

### Suggested Fix
Create a resilient market-brief data-source order: Treasury XML + Stooq per-symbol + CoinGecko first; then news pages; avoid relying on DuckDuckGo/Yahoo chart API during cron.

### Metadata
- Reproducible: yes
- Tags: web_search, web_fetch, market-brief, cron, rate-limit
- See Also: ERR-20260511-001

---
## [ERR-20260514-001] laravel_test_timestamp_mass_assignment

**Logged**: 2026-05-14T06:03:00+07:00
**Priority**: medium
**Status**: pending
**Area**: tests

### Summary
Feature test expected a manually backdated Eloquent `created_at`, but `create([...])` ignored the timestamp because the model fillable list does not include timestamp columns.

### Error
```
Expected response to contain: 5 days open
Actual rendered aging cue: 0 days open
```

### Context
- Command attempted: `php artisan test --filter=OperatorValidationPageTest`
- Slice: operator validation unresolved-aging cues
- Related file: `tests/Feature/OperatorValidationPageTest.php`

### Suggested Fix
Create the model first, then update timestamps with `forceFill([...])->saveQuietly()` or a direct query update when tests need controlled `created_at` values.

### Metadata
- Reproducible: yes
- Related Files: tests/Feature/OperatorValidationPageTest.php, app/Models/OperatorValidationFinding.php

---
## [ERR-20260515-001] repo_path_mismatch

**Logged**: 2026-05-15T14:46:00+07:00
**Priority**: low
**Status**: pending
**Area**: ops

### Summary
Daily autonomous_trading_ai cron prompt referenced workspace path that does not exist; long-term memory path was correct.

### Error
```
Get-ChildItem : Cannot find path 'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai' because it does not exist.
```

### Context
- Task: daily autonomous_trading_ai governance audit
- Actual repo found at `C:\laragon\www\autonomous_trading_ai`

### Suggested Fix
Update cron/task instructions to use the current repo path or add an explicit fallback note.

### Metadata
- Reproducible: yes
- Related Files: MEMORY.md
- Tags: autonomous_trading_ai, cron, path

---
## [ERR-20260515-001] market_brief_search_and_source_failures_recurring

**Logged**: 2026-05-15T14:56:00+07:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Morning Market Brief again hit `web_search` DNS failure and blocked market pages; Yahoo quote endpoint returned 401, while Yahoo chart endpoint worked.

### Error
```
web_search: getaddrinfo ENOTFOUND html.duckduckgo.com
web_fetch Investing.com: 403 / Just a moment
Yahoo quote API: HTTP Error 401: Unauthorized
PowerShell rejected bash-style heredoc: python - <<'PY'
```

### Context
- Direct Yahoo chart API (`/v8/finance/chart/{symbol}?range=5d&interval=1d`) worked for GC=F, BTC-USD, ES=F, DX-Y.NYB, ^TNX, CL=F, ^GSPC.
- TradingEconomics calendar page worked for extracting today’s macro watchouts.

### Suggested Fix
For market brief cron, implement/use a local helper that starts with Yahoo chart API + TradingEconomics calendar and avoids bash heredocs in PowerShell.

### Metadata
- Reproducible: yes
- Tags: web_search, yahoo, investing, market-brief, powershell, cron
- See Also: ERR-20260514-002

---

## [ERR-20260515-001] live_market_data_lookup

**Logged**: 2026-05-15T14:58:00+07:00
**Priority**: medium
**Status**: pending
**Area**: tools

### Summary
Urgent market-data lookup for Afu failed due to provider/API connectivity and rate limits.

### Details
- PowerShell rejected Bash-style `python - <<'PY'` heredoc; use temp files or `python -c` single-line in PowerShell.
- Yahoo Finance chart endpoint returned HTTP 429 for multiple symbols.
- Binance public API and web_search failed DNS resolution (`getaddrinfo` / `ENOTFOUND`).

### Suggested Action
For urgent trading/market briefs, prefer configured broker/exchange CLI/API if available; otherwise use a resilient quote adapter with multiple fallbacks and cached last-known data.

### Metadata
- Source: error
- Related Files: tmp/quote_check.py
- Tags: powershell, market-data, yahoo-finance, dns, rate-limit
---

## [ERR-20260515-002] github_bounty_search_stdout_rate_limit

**Logged**: 2026-05-15T17:47:00+07:00
**Priority**: low
**Status**: pending
**Area**: tools

### Summary
GitHub bounty scouting partially succeeded but hit unauthenticated API rate limits and Windows console Unicode encoding issues.

### Details
- GitHub API search worked initially and returned candidate bounty issues.
- Printing Unicode arrows on Windows cp1252 stdout caused `UnicodeEncodeError`; set `sys.stdout.reconfigure(encoding='utf-8')` in scripts.
- Further unauthenticated GitHub API searches returned HTTP 403 rate limit exceeded.

### Suggested Action
Use authenticated GitHub token for sustained issue scouting; default Python helper scripts should set UTF-8 stdout on Windows.

### Metadata
- Source: error
- Related Files: tmp/github_bounty_search.py, tmp/github_bounty_search2.py
- Tags: github-api, rate-limit, windows, unicode
---

## [ERR-20260515-003] web_search_dns_failure

**Logged**: 2026-05-15T17:50:00+07:00
**Priority**: low
**Status**: pending
**Area**: tools

### Summary
Web search failed during bounty scouting due to DuckDuckGo DNS resolution errors.

### Error
```
getaddrinfo ENOTFOUND html.duckduckgo.com
```

### Context
- Operation attempted: web_search for Algora/Polar/GitHub bounty issues
- Environment: OpenClaw subagent on Windows, Asia/Jakarta

### Suggested Fix
Fall back to direct GitHub/Algora/Polar page fetches or GitHub API/CLI; retry search later if DNS recovers.

### Metadata
- Reproducible: unknown
- Related Files: none
- Tags: web_search, dns, bounty-scouting
---

## 2026-05-15 - jlcsearch bounty local validation blockers

- Context: While fixing `tmp\bounty-jlcsearch` issue #92, root project validation could not use the normal toolchain locally.
- Failures:
  - `bun` is unavailable on this Windows host, so Bun-native scripts/tests cannot run.
  - `npm install --package-lock=false` failed on root due `kysely-bun-sqlite` peer conflict with `kysely@0.28.x`.
  - Retrying with `--legacy-peer-deps` reached `better-sqlite3` native build and failed because Visual Studio C++ build tools are missing for Node 25.
- Workaround: verify the Cloudflare proxy package independently with npm-installed deps: `npx tsc --noEmit` and `npx vitest run` in `cf-proxy`.
- Follow-up: For Bun-first projects, prefer installing/using Bun or a Node version with available native prebuilds before attempting root npm validation.
---
## [ERR-20260517-001] cron_edit_message_argument_windows

**Logged**: 2026-05-17T10:20:00+07:00
**Priority**: low
**Status**: workaround-found
**Area**: cli/windows

### Summary
Editing an OpenClaw cron job with a long/multiline --message from PowerShell caused commander parsing errors: "too many arguments for 'edit'". Direct Node spawn through the OpenClaw JS entrypoint worked after flattening the message to a single line.

### Suggested Fix
For long cron messages on Windows, write the message to tmp, then invoke node C:/Users/afusi/AppData/Roaming/npm/node_modules/openclaw/openclaw.mjs via a small Node script with an argv array. Avoid passing multiline text directly through PowerShell.

### Metadata
- Tags: openclaw, cron, windows, powershell, cli
---
## [ERR-20260517-002] pdf_tool_document_extract_unavailable

**Logged**: 2026-05-17T17:10:00+07:00
**Priority**: low
**Status**: workaround-found
**Area**: tools

### Summary
The `pdf` tool failed on an inbound CV PDF because document extraction is disabled/unavailable: enable the document-extract plugin to process application/pdf files.

### Details
Fallback worked using local `pdftotext.exe` available at `C:\laragon\bin\git\mingw64\bin\pdftotext.exe`, writing extracted text to `tmp/`.

### Suggested Action
When PDF extraction is unavailable, use local `pdftotext` for text-based PDFs before concluding the document cannot be read.

### Metadata
- Source: error
- Tags: pdf, document-extract, pdftotext, telegram-attachment

## 2026-05-18 - web_search provider DNS failure
- Context: researching trading indicators for Afu.
- Tool: web_search
- Error: getaddrinfo ENOTFOUND html.duckduckgo.com
- Mitigation: continued using successful web_fetch sources and internal market-structure knowledge; do not block user-facing work on one search provider failure.
