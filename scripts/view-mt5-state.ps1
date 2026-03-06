param(
    [string]$Url = "http://127.0.0.1:5001/state"
)

try {
    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -ErrorAction Stop
} catch {
    Write-Host "[ERROR] Failed to reach MT5 bridge at $Url" -ForegroundColor Red
    Write-Host "        $_" -ForegroundColor DarkRed
    exit 1
}

try {
    $data = $response.Content | ConvertFrom-Json
} catch {
    Write-Host "[ERROR] Failed to parse JSON from MT5 bridge" -ForegroundColor Red
    Write-Host $response.Content
    exit 1
}

"=== MT5 ACCOUNT STATE ==="
"Server time : {0}" -f $data.server_time
"Login       : {0}" -f $data.account.login
"Name        : {0}" -f $data.account.name
"Broker      : {0}" -f $data.account.company
"Balance     : {0}" -f $data.account.balance
"Equity      : {0}" -f $data.account.equity
"Margin      : {0}" -f $data.account.margin
"Free margin : {0}" -f $data.account.margin_free
"Leverage    : {0}" -f $data.account.leverage
"Currency    : {0}" -f $data.account.currency
" "

"Open positions:" 
if (-not $data.positions -or $data.positions.Count -eq 0) {
    "  (none)"
} else {
    $data.positions | ForEach-Object {
        $dir = if ($_.type -eq 0) { "BUY " } elseif ($_.type -eq 1) { "SELL" } else { $_.type }
        "  #{0} {1} {2} {3} lots @ {4} (SL: {5}, TP: {6}) PnL: {7}" -f `
            $_.ticket, $_.symbol, $dir, $_.volume, $_.price_open, $_.sl, $_.tp, $_.profit
    }
}