$ErrorActionPreference = "Stop"

$workspace = "C:\Users\afusi\.openclaw\workspace"
$python = Join-Path $workspace ".venv-chroma\Scripts\python.exe"
$script = Join-Path $workspace "scripts\chroma_ingest.py"
$logDir = Join-Path $workspace "memory"
$logFile = Join-Path $logDir "chroma_ingest.log"

if (!(Test-Path $logDir)) {
  New-Item -ItemType Directory -Path $logDir | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
  $output = & $python $script 2>&1
  Add-Content -Path $logFile -Value "[$timestamp] OK  $output"
}
catch {
  Add-Content -Path $logFile -Value "[$timestamp] ERROR  $($_.Exception.Message)"
  throw
}
