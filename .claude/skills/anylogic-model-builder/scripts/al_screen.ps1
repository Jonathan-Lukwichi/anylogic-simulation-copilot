# al_screen.ps1 - see and drive AnyLogic on this PC (Windows). Safety rules built in:
#  * mouse/keyboard commands act ONLY while the foreground window belongs to AnyLogic (the IDE, or a model
#    window "<model> : Simulation"); otherwise nothing happens and the script exits 2 - so the user can stop the
#    agent at any time just by clicking another window;
#  * captures are of AnyLogic windows only (by window handle); a browser showing a model is cropped below the
#    tab strip, so the user's other tabs are not captured.
#
#   al_screen.ps1 info                         foreground window: title, process, rectangle
#   al_screen.ps1 snap  <out.png> [ide|model]  capture the IDE or the running model by handle (works behind other windows)
#   al_screen.ps1 front [ide|model]            ask Windows to bring it to the front (Windows may refuse while the user types)
#   al_screen.ps1 shot  <out.png>              capture the AnyLogic window that is in front
#   al_screen.ps1 click|dbl|right <x> <y>      mouse at screen pixels (physical; DPI-aware)
#   al_screen.ps1 drag  <x> <y> <x2> <y2>
#   al_screen.ps1 keys  <SendKeys>             e.g. "{F5}" (run), "^s" (save)
# Image -> screen pixels: screenX = left + imgX / scale (printed with every capture).
param([string]$Cmd, [string]$A1, [string]$A2, [string]$A3, [string]$A4)
$ErrorActionPreference = 'Stop'
$cache = Join-Path (Split-Path $PSScriptRoot -Parent) '.cache'
New-Item -ItemType Directory -Force $cache | Out-Null
$dll = Join-Path $cache 'ALWin.dll'
if (-not (Test-Path $dll)) {
  Add-Type -ReferencedAssemblies System.Drawing -OutputAssembly $dll -OutputType Library -TypeDefinition @"
using System; using System.Drawing; using System.Runtime.InteropServices; using System.Text;
public static class ALWin {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  public struct RECT { public int Left, Top, Right, Bottom; }
  public static Bitmap Capture(IntPtr h) {
    RECT r; GetWindowRect(h, out r);
    var bmp = new Bitmap(Math.Max(1, r.Right - r.Left), Math.Max(1, r.Bottom - r.Top));
    using (var g = Graphics.FromImage(bmp)) { var hdc = g.GetHdc(); PrintWindow(h, hdc, 2); g.ReleaseHdc(hdc); }
    return bmp; }
}
"@
}
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type -Path $dll
[ALWin]::SetProcessDPIAware() | Out-Null
$AL = 'C:\Program Files\AnyLogic 8*'

function Find-Target($which) {
  if ($which -eq 'model') {
    foreach ($p in Get-Process) { if ($p.MainWindowTitle -like '* : Simulation*' -and $p.ProcessName -ne 'AnyLogic') { return $p } }
    return $null
  }
  Get-Process AnyLogic -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
}
function Describe($h) {
  $fpid = [uint32]0; [ALWin]::GetWindowThreadProcessId($h, [ref]$fpid) | Out-Null
  $proc = Get-Process -Id $fpid -ErrorAction SilentlyContinue
  $path = try { $proc.Path } catch { '' }
  $sb = New-Object System.Text.StringBuilder 512; [ALWin]::GetWindowText($h, $sb, 512) | Out-Null
  $r = New-Object ALWin+RECT; [ALWin]::GetWindowRect($h, [ref]$r) | Out-Null
  [pscustomobject]@{ Title = $sb.ToString(); Proc = $proc.ProcessName; R = $r; W = $r.Right - $r.Left; H = $r.Bottom - $r.Top
    IsAL = ($proc.ProcessName -match '^AnyLogic') -or ($path -like $AL) -or ($sb.ToString() -like '* : Simulation*') }
}
function Save-Scaled($bmp, $out, $cropTop, $max) {
  $src = $bmp
  if ($cropTop -gt 0) { $src = $bmp.Clone((New-Object System.Drawing.Rectangle 0, $cropTop, $bmp.Width, ($bmp.Height - $cropTop)), $bmp.PixelFormat) }
  $scale = [math]::Min(1.0, $max / $src.Width)
  $dst = New-Object System.Drawing.Bitmap ([int]($src.Width * $scale)), ([int]($src.Height * $scale))
  $g = [System.Drawing.Graphics]::FromImage($dst); $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.DrawImage($src, 0, 0, $dst.Width, $dst.Height); $dst.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
  return $scale
}

switch ($Cmd) {
  'snap' {
    $which = if ($A2) { $A2 } else { 'ide' }
    $p = Find-Target $which
    if (-not $p) { "no $which window found"; exit 3 }
    $crop = if ($which -eq 'model' -and $p.MainWindowTitle -match 'Microsoft.?Edge|Google Chrome|Mozilla Firefox|Brave|Opera') { 110 } else { 0 }
    $bmp = [ALWin]::Capture($p.MainWindowHandle)
    $s = Save-Scaled $bmp $A1 $crop 1600
    "saved $A1 from '$($p.MainWindowTitle)' [$($p.ProcessName)] window $($bmp.Width)x$($bmp.Height), top $crop px cropped, scale $s"
    exit 0
  }
  'front' {
    $which = if ($A1) { $A1 } else { 'ide' }
    $p = Find-Target $which
    if (-not $p) { "no $which window found"; exit 3 }
    [ALWin]::ShowWindow($p.MainWindowHandle, 9) | Out-Null
    (New-Object -ComObject WScript.Shell).AppActivate($p.Id) | Out-Null
    [ALWin]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
    Start-Sleep -Milliseconds 700
    $d = Describe ([ALWin]::GetForegroundWindow())
    "front now: '$($d.Title)' [$($d.Proc)] (anylogic=$($d.IsAL))"
    exit 0
  }
}

$d = Describe ([ALWin]::GetForegroundWindow())
"foreground: '$($d.Title)' [$($d.Proc)] rect=($($d.R.Left),$($d.R.Top))-($($d.R.Right),$($d.R.Bottom)) anylogic=$($d.IsAL)"
if ($Cmd -eq 'info') { exit 0 }
if (-not $d.IsAL) { "STOP: AnyLogic is not the active window - nothing done."; exit 2 }
function Btn($down, $up) { [ALWin]::mouse_event($down, 0, 0, 0, [IntPtr]::Zero); Start-Sleep -Milliseconds 60; [ALWin]::mouse_event($up, 0, 0, 0, [IntPtr]::Zero) }
switch ($Cmd) {
  'shot' {
    if ($d.W -lt 50 -or $d.H -lt 50) { "STOP: active AnyLogic window too small ($($d.W)x$($d.H)) - use 'front' first"; exit 4 }
    $bmp = New-Object System.Drawing.Bitmap $d.W, $d.H
    [System.Drawing.Graphics]::FromImage($bmp).CopyFromScreen($d.R.Left, $d.R.Top, 0, 0, (New-Object System.Drawing.Size $d.W, $d.H))
    # a browser showing a model: crop the tab strip and address bar (the user's other tabs stay private)
    $crop = if ($d.Title -match 'Microsoft.?Edge|Google Chrome|Mozilla Firefox|Brave|Opera') { 110 } else { 0 }
    $s = Save-Scaled $bmp $A1 $crop 1600
    "saved $A1 ; screenX = $($d.R.Left) + imgX / $s ; screenY = $($d.R.Top + $crop) + imgY / $s"
  }
  'click' { [ALWin]::SetCursorPos([int]$A1, [int]$A2) | Out-Null; Start-Sleep -Milliseconds 120; Btn 0x2 0x4; "clicked $A1,$A2" }
  'dbl'   { [ALWin]::SetCursorPos([int]$A1, [int]$A2) | Out-Null; Start-Sleep -Milliseconds 120; Btn 0x2 0x4; Start-Sleep -Milliseconds 90; Btn 0x2 0x4; "double-clicked $A1,$A2" }
  'right' { [ALWin]::SetCursorPos([int]$A1, [int]$A2) | Out-Null; Start-Sleep -Milliseconds 120; Btn 0x8 0x10; "right-clicked $A1,$A2" }
  'drag'  {
    [ALWin]::SetCursorPos([int]$A1, [int]$A2) | Out-Null; Start-Sleep -Milliseconds 150
    [ALWin]::mouse_event(0x2, 0, 0, 0, [IntPtr]::Zero); Start-Sleep -Milliseconds 150
    for ($i = 1; $i -le 20; $i++) { [ALWin]::SetCursorPos([int]([int]$A1 + ([int]$A3 - [int]$A1) * $i / 20), [int]([int]$A2 + ([int]$A4 - [int]$A2) * $i / 20)) | Out-Null; Start-Sleep -Milliseconds 25 }
    Start-Sleep -Milliseconds 150; [ALWin]::mouse_event(0x4, 0, 0, 0, [IntPtr]::Zero); "dragged $A1,$A2 -> $A3,$A4"
  }
  'keys'  { [System.Windows.Forms.SendKeys]::SendWait($A1); "sent keys $A1" }
  default { "unknown command '$Cmd' - see the header of this script" ; exit 1 }
}

