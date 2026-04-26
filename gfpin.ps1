# gfpin recipe -- edit the variables below, then run: .\gfpin.ps1
# Copy this file and rename it (e.g. drawer-pin.ps1) to save a recipe.
# Re-running the same script regenerates the same object.

# NOTE: this URL points at the bitranox fork's `py314compat` branch, which
# carries the not-yet-upstreamed Python 3.13 / 3.14 compatibility patches
# (PaulBone/gfthings#9). Once that PR is merged upstream, replace the
# value below with one of:
#   $GfthingsSource = 'git+https://github.com/PaulBone/gfthings.git'   # or @main
#   $GfthingsSource = 'gfthings'                                       # once a PyPI release ships
$GfthingsSource = 'git+https://github.com/bitranox/gfthings.git@py314compat'

# ---- Output ----
$Format = 'step'   # 'step' or 'stl'
$VsCode = 0        # >0 = run in vscode_ocp mode on that port (no file produced)

# ---------- output filename (auto-derived) ----------
$basename = "pin.${Format}"
$Output   = Join-Path $PSScriptRoot $basename
# To override, set $Output = 'mycustomname.step' here.

# ---------- build args ----------
$cliArgs = @('-o', $Output)
if ($VsCode -gt 0) { $cliArgs += @('--vscode', $VsCode) }

# ---------- invoke ----------
$inv = [System.Globalization.CultureInfo]::InvariantCulture
$displayArgs = $cliArgs | ForEach-Object {
    if ($_ -is [double] -or $_ -is [single] -or $_ -is [decimal]) { ([double]$_).ToString($inv) } else { "$_" }
}
Write-Host "uvx --from $GfthingsSource gfpin $($displayArgs -join ' ')"
& uvx --from $GfthingsSource gfpin @cliArgs
if ($LASTEXITCODE -eq 0) { Write-Host "Wrote: $Output" }
