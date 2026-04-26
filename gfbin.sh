#!/usr/bin/env bash
# gfbin recipe -- edit the variables below, then run: ./gfbin.sh
# Copy this file and rename it (e.g. screws-bin-2x2x4.sh) to save a recipe.
# Re-running the same script regenerates the same object.

set -euo pipefail

# NOTE: this URL points at the bitranox fork's `py314compat` branch, which
# carries the not-yet-upstreamed Python 3.13 / 3.14 compatibility patches
# (PaulBone/gfthings#9). Once that PR is merged upstream, replace the
# value below with one of:
#   GfthingsSource='git+https://github.com/PaulBone/gfthings.git'      # or @main
#   GfthingsSource='gfthings'                                          # once a PyPI release ships
GfthingsSource='git+https://github.com/bitranox/gfthings.git@py314compat'

# ---- Bin dimensions (gridfinity units) ----
X=1   # width
Y=1   # depth
Z=4   # height (min 3)

# ---- Interior ----
Scoop=12.5      # scoop radius in mm (0 = none)
Divisions=1     # internal divisions (3+ per unit not recommended)
NoLabel=false   # omit label shelf
NoLip=false     # omit stacking lip
HalfWall=false  # half walls (link bins end-to-end)

# ---- Magnets / base ----
NoMagnet=false      # skip magnet holes entirely
Unrefined=false     # circular holes instead of refined slots
MagnetDia=6         # mm
MagnetHeight=2      # mm
HalfGrid=false      # 21mm units (may break magnet holes)
WallThickness=1.2   # mm

# ---- Special ----
Funky=''   # python expr for non-rectangular shape (ignores X/Y/divisions); '' to skip

# ---- Output ----
Format='step'   # 'step' or 'stl'
Loop=false      # batch-generate variants (names as bin_*.step)
VsCode=0        # >0 = run in vscode_ocp mode on that port (no file produced)

# ---------- output filename (auto-derived from params) ----------
ScriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tags=()
[[ "$NoLabel"   == 'true' ]] && tags+=( 'nolabel' )
[[ "$NoLip"     == 'true' ]] && tags+=( 'nolip' )
[[ "$HalfWall"  == 'true' ]] && tags+=( 'halfwall' )
[[ "$NoMagnet"  == 'true' ]] && tags+=( 'nomagnet' )
[[ "$Unrefined" == 'true' ]] && tags+=( 'unrefined' )
[[ "$HalfGrid"  == 'true' ]] && tags+=( 'halfgrid' )
[[ -n "$Funky" ]]            && tags+=( "funky-${Funky}" )
if (( ${#tags[@]} )); then
    tagSuffix="_$(IFS=_; echo "${tags[*]}")"
else
    tagSuffix=''
fi
basename="bin_${X}x${Y}x${Z}_div${Divisions}_scoop${Scoop}_mag${MagnetDia}x${MagnetHeight}_wall${WallThickness}${tagSuffix}.${Format}"
Output="${ScriptDir}/${basename}"
# To override, set Output='mycustomname.step' here.

# ---------- build args ----------
cliArgs=(
    '-x' "$X" '-y' "$Y" '-z' "$Z"
    '--scoop'          "$Scoop"
    '--divisions'      "$Divisions"
    '--magnet-dia'     "$MagnetDia"
    '--magnet-height'  "$MagnetHeight"
    '--wall-thickness' "$WallThickness"
    '-o' "$Output"
)
[[ "$NoLabel"   == 'true' ]] && cliArgs+=( '--no-label' )
[[ "$NoLip"     == 'true' ]] && cliArgs+=( '--no-lip' )
[[ "$HalfWall"  == 'true' ]] && cliArgs+=( '--half-wall' )
[[ "$NoMagnet"  == 'true' ]] && cliArgs+=( '--no-magnet' )
[[ "$Unrefined" == 'true' ]] && cliArgs+=( '--unrefined' )
[[ "$HalfGrid"  == 'true' ]] && cliArgs+=( '--half-grid' )
[[ "$Loop"      == 'true' ]] && cliArgs+=( '--loop' )
[[ -n "$Funky" ]]            && cliArgs+=( '--funky' "$Funky" )
if [[ "$VsCode" -gt 0 ]]; then cliArgs+=( '--vscode' "$VsCode" ); fi

# ---------- invoke ----------
echo "uvx --from $GfthingsSource gfbin ${cliArgs[*]}"
uvx --from "$GfthingsSource" gfbin "${cliArgs[@]}"
echo "Wrote: $Output"
