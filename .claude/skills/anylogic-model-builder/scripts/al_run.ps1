# al_run.ps1 - open, check and unblock AnyLogic model runs on this PC (Windows).
#
#   al_run.ps1 open <model.alp>    open the model in AnyLogic THROUGH WINDOWS EXPLORER (the user's session).
#                                  Never start anylogic.exe from an agent's shell: the model window
#                                  (built-in browser) cannot start from there and every run hangs (gotcha G124).
#   al_run.ps1 status              AnyLogic + every running model: start time, port, CPU, and whether it is
#                                  simulating or waiting for its window (thread dump via the bundled jstack)
#   al_run.ps1 window              for each model waiting for its window: open http://127.0.0.1:<port>/ through
#                                  Explorer (the user's default browser) - the model then starts (G124 fix)
#   al_run.ps1 log [n]             last n lines of AnyLogic's workspace log (build/run messages, exceptions)
#   al_run.ps1 stop                stop model processes started by AnyLogic (not AnyLogic itself)
param([string]$Cmd, [string]$A1)
$inst = Get-ChildItem 'C:\Program Files' -Directory -Filter 'AnyLogic 8*' | Sort-Object Name -Descending | Select-Object -First 1
$jstack = Join-Path $inst.FullName 'jre\bin\jstack.exe'
$ws = Get-ChildItem $env:USERPROFILE -Directory -Force -Filter '.AnyLogic*' | ForEach-Object { Get-ChildItem $_.FullName -Directory -Filter 'Workspace*' } | Sort-Object LastWriteTime -Descending | Select-Object -First 1

function Get-Models {
  Get-CimInstance Win32_Process -Filter "Name='javaw.exe' OR Name='java.exe'" | Where-Object { $_.CommandLine -match 'com\.anylogic\.ms\.MS\s+(\S+)' } | ForEach-Object {
    $exp = $Matches[1]
    $port = (Get-NetTCPConnection -OwningProcess $_.ProcessId -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1).LocalPort
    $dump = if (Test-Path $jstack) { & $jstack $_.ProcessId 2>&1 | Out-String } else { '' }
    $state = if ($dump -match 'Experiment\.waitFrontend') { 'WAITING FOR ITS WINDOW' } elseif ($dump -match 'com\.anylogic\.engine\.Engine') { 'running' } else { 'starting or unknown' }
    $p = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
    [pscustomobject]@{ Pid = $_.ProcessId; Experiment = $exp; Started = $_.CreationDate; Port = $port; CPU = [math]::Round($p.CPU, 1); State = $state }
  }
}

switch ($Cmd) {
  'open' {
    $f = Resolve-Path $A1 -ErrorAction Stop
    Start-Process explorer.exe -ArgumentList "`"$f`""
    "asked Windows Explorer to open $f (AnyLogic runs in the user's session)"
  }
  'status' {
    $al = Get-Process AnyLogic -ErrorAction SilentlyContinue
    if ($al) { "AnyLogic pid $($al.Id) since $($al.StartTime.ToString('HH:mm:ss')) : '$($al.MainWindowTitle)'" } else { "AnyLogic is not running" }
    $m = @(Get-Models)
    if (-not $m) { "no model is running" } else { $m | Format-Table Pid, Experiment, @{n='Started';e={$_.Started.ToString('HH:mm:ss')}}, Port, CPU, State -AutoSize | Out-String }
    $win = Get-Process | Where-Object { $_.MainWindowTitle -like '* : Simulation*' -and $_.ProcessName -ne 'AnyLogic' }
    if ($win) { "model window open in [$($win[0].ProcessName)]: '$($win[0].MainWindowTitle)'" }
  }
  'window' {
    $m = @(Get-Models | Where-Object { $_.State -eq 'WAITING FOR ITS WINDOW' -and $_.Port })
    if (-not $m) { "no model is waiting for its window"; exit 0 }
    foreach ($x in $m) {
      Start-Process explorer.exe -ArgumentList "http://127.0.0.1:$($x.Port)/"
      "opened http://127.0.0.1:$($x.Port)/ for $($x.Experiment) (pid $($x.Pid)) in the default browser"
    }
    Start-Sleep -Seconds 8
    Get-Models | Format-Table Pid, Experiment, Port, CPU, State -AutoSize | Out-String
  }
  'log' {
    $n = if ($A1) { [int]$A1 } else { 40 }
    $log = Join-Path $ws.FullName '.metadata\.log'
    "log: $log"; Get-Content $log -Tail $n
  }
  'stop' {
    $m = @(Get-Models)
    foreach ($x in $m) { Stop-Process -Id $x.Pid -ErrorAction SilentlyContinue; "stopped model run pid $($x.Pid) ($($x.Experiment))" }
    if (-not $m) { "no model run to stop" }
  }
  default { "usage: al_run.ps1 open <model.alp> | status | window | log [n] | stop"; exit 1 }
}
