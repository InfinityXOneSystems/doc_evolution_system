$ErrorActionPreference = "Stop"

$ROOT = "C:\AI\repos\doc_evolution_system"
$LOGS = Join-Path $ROOT "logs"
$SLEEP = 300
$PYTHON = "python"

New-Item -ItemType Directory -Force $LOGS | Out-Null

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Tee-Object -FilePath "$LOGS\docd.log" -Append
}

Log "🚀 docd daemon started"

while ($true) {
    try {
        Set-Location $ROOT

        $gate = & $PYTHON -c "from guards.workspace_gate import workspace_allows_execution; print('ALLOW' if workspace_allows_execution() else 'DENY')"
        if ($gate -notmatch "ALLOW") {
            Log "⛔ Workspace gate blocked execution"
            Start-Sleep -Seconds $SLEEP
            continue
        }

        Log "🔍 Running doc sync"
        & $PYTHON -c "import sys; sys.path.insert(0,'.'); from doc_sync.sync_orchestrator import run_local_doc_sync; run_local_doc_sync()"

        git add . | Out-Null
        git commit -m "docd: auto-heal cycle" 2>$null | Out-Null
        git push origin main 2>$null | Out-Null

        Log "✅ Cycle complete"
    }
    catch {
        Log "⚠️ ERROR: $($_.Exception.Message)"
    }

    Start-Sleep -Seconds $SLEEP
}
