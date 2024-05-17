from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from parameters import *
from Base import *

with BuildPart() as p:
    BaseSquare()
    with Locations((-bin_size/2, 0, -(plate_height + plate_base_height)/2 + 4.7)):
        ClipEdge(edge_cut_len, rotation=(0, 0, 0), align=(Align.MIN, Align.CENTER, Align.MAX))
    with Locations((bin_size/2, 0, -(plate_height + plate_base_height)/2 + 4.7)):
        ClipEdge(edge_cut_len, rotation=(0, 0, 180), align=(Align.MIN, Align.CENTER, Align.MAX))

show(p.part)
