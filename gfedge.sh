#!/usr/bin/env bash
# gfedge recipe -- edit the variables below, then run: ./gfedge.sh
# Copy this file and rename it (e.g. drawer-edge-4x14.sh) to save a recipe.
# Re-running the same script regenerates the same object.

set -euo pipefail

# NOTE: this URL points at the bitranox fork's `py314compat` branch, which
# carries the not-yet-upstreamed Python 3.13 / 3.14 compatibility patches
# (PaulBone/gfthings#9). Once that PR is merged upstream, replace the
# value below with one of:
#   GfthingsSource='git+https://github.com/PaulBone/gfthings.git'      # or @main
#   GfthingsSource='gfthings'                                          # once a PyPI release ships
GfthingsSource='git+https://github.com/bitranox/gfthings.git@py314compat'

# ---- Dimensions ----
X=4         # gridfinity units across
Y=16        # depth in mm
Short=false # short variant (no screw holes)

# ---- Output ----
Format='step'   # 'step' or 'stl'
Loop=false      # batch-generate variants
VsCode=0        # >0 = run in vscode_ocp mode on that port (no file produced)

# ---------- output filename (auto-derived from params) ----------
ScriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tags=()
[[ "$Short" == 'true' ]] && tags+=( 'short' )
if (( ${#tags[@]} )); then
    tagSuffix="_$(IFS=_; echo "${tags[*]}")"
else
    tagSuffix=''
fi
basename="edge_${X}x${Y}${tagSuffix}.${Format}"
Output="${ScriptDir}/${basename}"
# To override, set Output='mycustomname.step' here.

# ---------- build args ----------
cliArgs=( '-x' "$X" '-y' "$Y" '-o' "$Output" )
[[ "$Short" == 'true' ]] && cliArgs+=( '--short' )
[[ "$Loop"  == 'true' ]] && cliArgs+=( '--loop' )
if [[ "$VsCode" -gt 0 ]]; then cliArgs+=( '--vscode' "$VsCode" ); fi

# ---------- invoke ----------
echo "uvx --from $GfthingsSource gfedge ${cliArgs[*]}"
uvx --from "$GfthingsSource" gfedge "${cliArgs[@]}"
echo "Wrote: $Output"
