# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid

from .parameters import *
from .Base import *

class EdgeSpacer(BasePartObject):
    def __init__(self, space : float, short : bool = False, crossbar : bool = False,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        clip_len = 16.5
        structure_thickness = plate_base_height(False)
        with BuildPart() as p:
            Box(structure_thickness, bin_size, plate_base_height(short))
            with Locations((-structure_thickness/2, 
                            0, 
                            -plate_base_height(short)/2 + 4.7 - plate_base_height(False) + plate_base_height(short))):
                ClipEdge(clip_len+1, align=(Align.MIN, Align.CENTER, Align.MAX))
                with Locations((0, -clip_len/2, 0)):
                    Box(structure_thickness, (bin_size - clip_len)/2, 2,
                        align=(Align.MIN, Align.MAX, Align.MAX))
                with Locations((0, clip_len/2, 0)):
                    Box(structure_thickness, (bin_size - clip_len)/2, 2,
                        align=(Align.MIN, Align.MIN, Align.MAX))
            fillet(edges().filter_by(Axis.Y)
                          .group_by(Axis.X)[-1]
                          .group_by(Axis.Z)[-1],
                   radius=1)

            space_height = plate_base_height(False) if not short else 1.6
            with Locations((-structure_thickness/2,
                            -bin_size/2,
                            -plate_base_height(short)/2)):
                Box(space, structure_thickness, space_height,
                    align=(Align.MIN, Align.MIN, Align.MIN))
            with Locations((-structure_thickness/2,
                            bin_size/2,
                            -plate_base_height(short)/2)):
                Box(space, structure_thickness, space_height,
                    align=(Align.MIN, Align.MAX, Align.MIN))
            if crossbar:
                with Locations((-structure_thickness/2,
                                0,
                                -plate_base_height(short)/2)):
                    Box(space, structure_thickness*2, space_height,
                        align=(Align.MIN, Align.CENTER, Align.MIN))
            with Locations((space - structure_thickness/2,
                            0,
                            -plate_base_height(short)/2)):
                Box(structure_thickness, bin_size, space_height,
                    align=(Align.MAX, Align.CENTER, Align.MIN))

            z_fillet_rad = min(2, space/2 - plate_base_height(short) - 2)
            fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[1] + 
                   edges().filter_by(Axis.Z).group_by(Axis.Y)[-2],
                   radius=z_fillet_rad)
            if crossbar:
                fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[4] +
                       edges().filter_by(Axis.Z).group_by(Axis.Y)[5],
                       radius=z_fillet_rad)

        super().__init__(p.part, rotation, align, mode)

class Edge(BasePartObject):
    def __init__(self, units : int, space : float,
                 short : bool = False,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            with GridLocations(bin_size, bin_size, 1, units):
                EdgeSpacer(space, short=short)

        super().__init__(p.part, rotation, align, mode)
        
if __name__ == "__main__":
    e = Edge(4, 22)
    from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
    set_port(3939)
    show_object(e)
    
