# gfbase recipe -- edit the variables below, then run: .\gfbase.ps1
# Copy this file and rename it (e.g. drawer-base-4x3.ps1) to save a recipe.
# Re-running the same script regenerates the same object.

# NOTE: this URL points at the bitranox fork's `py314compat` branch, which
# carries the not-yet-upstreamed Python 3.13 / 3.14 compatibility patches
# (PaulBone/gfthings#9). Once that PR is merged upstream, replace the
# value below with one of:
#   $GfthingsSource = 'git+https://github.com/PaulBone/gfthings.git'   # or @main
#   $GfthingsSource = 'gfthings'                                       # once a PyPI release ships
$GfthingsSource = 'git+https://github.com/bitranox/gfthings.git@py314compat'

# ---- Dimensions ----
$X = 4   # gridfinity units across
$Y = 4   # gridfinity units deep

# ---- Holes ----
$ScrewDiameter           = 4      # mm
$MagnetDiameter          = 6.2    # mm (or countersink diameter)
$MagnetDepth             = 2      # mm
$ScrewHoleCount          = 2      # 0, 2, or 4 per grid square
$ScrewHolePatternDrawer  = $false # add 4 extra screw holes in drawer pattern
$NoMagnet                = $false # skip magnet pocket (screw holes kept as plain holes)

# ---- Variant ----
$Short = $false  # short variant (no screw holes)

# ---- Output ----
$Format = 'step'   # 'step' or 'stl'
$Loop   = $false   # batch-generate variants
$VsCode = 0        # >0 = run in vscode_ocp mode on that port (no file produced)

# ---------- output filename (auto-derived from params) ----------
$tags = @()
if ($ScrewHolePatternDrawer) { $tags += 'drawer' }
if ($NoMagnet)               { $tags += 'nomagnet' }
if ($Short)                  { $tags += 'short' }
$tagSuffix = if ($tags) { '_' + ($tags -join '_') } else { '' }
$basename  = "base_${X}x${Y}_screw${ScrewDiameter}_mag${MagnetDiameter}x${MagnetDepth}_holes${ScrewHoleCount}${tagSuffix}.${Format}"
$Output    = Join-Path $PSScriptRoot $basename
# To override, set $Output = 'mycustomname.step' here.

# ---------- build args ----------
$cliArgs = @(
    '-x', $X, '-y', $Y,
    '--screw-diameter',  $ScrewDiameter,
    '--magnet-diameter', $MagnetDiameter,
    '--magnet-depth',    $MagnetDepth,
    '--screw-hole-count', $ScrewHoleCount,
    '-o', $Output
)
if ($ScrewHolePatternDrawer) { $cliArgs += '--screw-hole-pattern-drawer' }
if ($NoMagnet)               { $cliArgs += '--no-magnet' }
if ($Short)                  { $cliArgs += '--short' }
if ($Loop)                   { $cliArgs += '--loop' }
if ($VsCode -gt 0)           { $cliArgs += @('--vscode', $VsCode) }

# ---------- invoke ----------
$inv = [System.Globalization.CultureInfo]::InvariantCulture
$displayArgs = $cliArgs | ForEach-Object {
    if ($_ -is [double] -or $_ -is [single] -or $_ -is [decimal]) { ([double]$_).ToString($inv) } else { "$_" }
}
Write-Host "uvx --from $GfthingsSource gfbase $($displayArgs -join ' ')"
& uvx --from $GfthingsSource gfbase @cliArgs
if ($LASTEXITCODE -eq 0) { Write-Host "Wrote: $Output" }
