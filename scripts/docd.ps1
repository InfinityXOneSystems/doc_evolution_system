# ======================================================================
# 🔱 DOC EVOLUTION DAEMON (docd)
# MODE: FAANG • IMMORTAL • TRI-WAY • SELF-HEALING
# ======================================================================

$ErrorActionPreference = "Stop"

$ROOT = "C:\AI\repos\doc_evolution_system"
$LOGS = Join-Path $ROOT "logs"
$SLEEP_SECONDS = 300  # 5 minutes

New-Item -ItemType Directory -Force $LOGS | Out-Null

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Tee-Object -FilePath "$LOGS\docd.log" -Append
}

Log "🚀 docd daemon started"

while ($true) {
    try {
        Set-Location $ROOT

        Log "🔍 Running doc sync cycle"

        python -c "
import sys
sys.path.insert(0,'.')
from doc_sync.sync_orchestrator import run_local_doc_sync
run_local_doc_sync()
print('SYNC_OK')
"

        Log "📦 Git sync"
        git add . | Out-Null
        git commit -m \"docd: automated doc evolution\" 2>$null | Out-Null
        git push origin main 2>$null | Out-Null

        Log "✅ cycle complete"
    }
    catch {
        Log \"⚠️ ERROR: $($_.Exception.Message)\"
    }

    Start-Sleep -Seconds $SLEEP_SECONDS
}
