# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from parameters import *
from Base import *

class VerticalScrewHole(BasePartObject):
    def __init__(self, width, height, screw_offset,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            Box(plate_base_height, width, height)
            fillet(edges().filter_by(Axis.X).group_by(Axis.Z)[-1],
                   radius=min(screw_support_fillet, width/2 - 0.1))
            with Locations(faces().filter_by(Plane.YZ).sort_by(Axis.X)[0]):
                with Locations((height/2 - screw_offset, 0)):
                    CounterSinkHole(screw_dia/2, magnet_dia/2)
            fillet(edges().filter_by(Plane.YZ).group_by(Axis.X)[0], radius=0.25)
        super().__init__(p.part, rotation, align, mode)

class EdgeSpacer(BasePartObject):
    def __init__(self, space : float,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        clip_len = 16.5
        structure_thickness = plate_base_height
        with BuildPart() as p:
            Box(structure_thickness, bin_size, plate_base_height)
            with Locations((-structure_thickness/2, 
                            0, 
                            -plate_base_height/2 + 4.7)):
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

            with Locations((-structure_thickness/2,
                            -bin_size/2,
                            -plate_base_height/2)):
                Box(space, structure_thickness, plate_base_height,
                    align=(Align.MIN, Align.MIN, Align.MIN))
            with Locations((-structure_thickness/2,
                            bin_size/2,
                            -plate_base_height/2)):
                Box(space, structure_thickness, plate_base_height,
                    align=(Align.MIN, Align.MAX, Align.MIN))
            with Locations((-structure_thickness/2, 0, -plate_base_height/2)):
                Box(space, structure_thickness*2, plate_base_height,
                    align=(Align.MIN, Align.CENTER, Align.MIN))
            with Locations((space - structure_thickness/2,
                            0,
                            -plate_base_height/2)):
                Box(plate_base_height, bin_size, plate_base_height,
                    align=(Align.MAX, Align.CENTER, Align.MIN))

            z_fillet_rad = min(2, space/2 - plate_base_height - 2)
            fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[1] + 
                   edges().filter_by(Axis.Z).group_by(Axis.Y)[-2],
                   radius=z_fillet_rad)
            fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[4] +
                   edges().filter_by(Axis.Z).group_by(Axis.Y)[5],
                   radius=z_fillet_rad)

# Exprimental feature, screw holes that let you attach to the side of
# drawers where the wood is likely thicker.
# Exprimental because the current version is too short to get my
# screwdriver in to access it and it's kind-of unnecessary anyway.
#           with Locations((space - structure_thickness/2,
#                           0,
#                           -plate_base_height/2)):
#               VerticalScrewHole(10, 15, 4, 
#                                 align=(Align.MAX, Align.CENTER, Align.MIN))

        super().__init__(p.part, rotation, align, mode)

for space in range(10, 20, 2):
    for num in range(4):
        with BuildPart() as p:
            with GridLocations(bin_size, bin_size, 1, num+1):
                EdgeSpacer(space)

        name = "edge_%d_x%d.step" % (space, num+1)
        export_step(p.part, name)
        show_object(p.part, name=name)

