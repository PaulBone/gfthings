#!/usr/bin/env bash
# gfpin recipe -- edit the variables below, then run: ./gfpin.sh
# Copy this file and rename it (e.g. drawer-pin.sh) to save a recipe.
# Re-running the same script regenerates the same object.

set -euo pipefail

# NOTE: this URL points at the bitranox fork's `py314compat` branch, which
# carries the not-yet-upstreamed Python 3.13 / 3.14 compatibility patches
# (PaulBone/gfthings#9). Once that PR is merged upstream, replace the
# value below with one of:
#   GfthingsSource='git+https://github.com/PaulBone/gfthings.git'      # or @main
#   GfthingsSource='gfthings'                                          # once a PyPI release ships
GfthingsSource='git+https://github.com/bitranox/gfthings.git@py314compat'

# ---- Output ----
Format='step'   # 'step' or 'stl'
VsCode=0        # >0 = run in vscode_ocp mode on that port (no file produced)

# ---------- output filename (auto-derived) ----------
ScriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
basename="pin.${Format}"
Output="${ScriptDir}/${basename}"
# To override, set Output='mycustomname.step' here.

# ---------- build args ----------
cliArgs=( '-o' "$Output" )
if [[ "$VsCode" -gt 0 ]]; then cliArgs+=( '--vscode' "$VsCode" ); fi

# ---------- invoke ----------
echo "uvx --from $GfthingsSource gfpin ${cliArgs[*]}"
uvx --from "$GfthingsSource" gfpin "${cliArgs[@]}"
echo "Wrote: $Output"
