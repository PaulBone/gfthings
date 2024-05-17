#
# Make a pin for holding a base plate to plywood.
#

from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from gfthings.parameters import *

with BuildPart() as p:
    import math

    total_height = 3.2 + plate_base_height + 0.5
    shaft_len = total_height - (magnet_dia - screw_dia)/2
    inner_shaft = 1.0
    outer_shaft = 1.7
    peg_rad = 0.5
    cut_width = 0.8
    
    with BuildSketch(Plane.XZ):
        with BuildLine() as f:
            
            Polyline((inner_shaft, -(outer_shaft - inner_shaft)),
                     (outer_shaft + peg_rad, peg_rad), 
                     (outer_shaft, peg_rad + math.tan(20*math.pi/180)*peg_rad),
                     (outer_shaft, peg_rad + shaft_len),
                     (magnet_dia/2-0.2, peg_rad + total_height),
                     (0, peg_rad + total_height),
                     (0, peg_rad + shaft_len),
                     (inner_shaft, peg_rad + shaft_len),
                     (inner_shaft, -(outer_shaft - inner_shaft)))
        make_face()
    revolve()
    with Locations((0, 0, -(peg_rad + (outer_shaft - inner_shaft)))):
        cut_len = 3*shaft_len/4 + peg_rad + (outer_shaft - inner_shaft)
        Box(50, cut_width, cut_len, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Box(cut_width, 50, cut_len, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))

def main():
    print("Writing pin object to pin.step")
    export_step(p.part, "pin.step")

