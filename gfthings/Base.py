# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid

from gfthings.parameters import *
from gfthings.GFProfile import GFProfilePlate

class ScrewSupport(BasePartObject):
    def __init__(self,
            rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
            align: Align | tuple[Align, Align, Align] = None,
            mode: Mode = Mode.ADD):
        with BuildPart() as p:
            Box(screw_hole_support, screw_hole_support, plate_base_height)
            fillet(edges(Select.LAST).filter_by(Axis.Z).group_by(Axis.X)[-1].
                        sort_by(Axis.Y)[-1],
                   radius=screw_support_fillet)
            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1]):
                offset = screw_offset - screw_hole_support/2
                with Locations((offset, offset)):
                    Hole(radius=screw_dia/2)
                    Hole(radius=magnet_dia/2, depth=2)
            fillet(edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
                   radius=0.25)
        super().__init__(p.part, rotation, align, mode)

class EdgeCut(BasePartObject):
    def __init__(self, cutout_long_len,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            import math
            tri_len = math.tan(30.0 * math.pi/180.0)*plate_height
            cutout_short_len = cutout_long_len - tri_len*2

            with Locations((0, 0, -3)):
                with BuildSketch(Plane.XY):
                    Rectangle(cutout_short_len, plate_height)
                    with Locations(
                            edges().filter_by(Axis.Y).sort_by(Axis.X)[0]@0.5):
                        Triangle(a=plate_height, b=tri_len, C=90,
                                 align=(Align.CENTER, Align.MIN),
                                 rotation=90)
                    with Locations(
                            edges().filter_by(Axis.Y).sort_by(Axis.X)[-1]@0.5):
                        Triangle(a=tri_len, b=plate_height, C=90,
                                 align=(Align.MAX, Align.CENTER),
                                 rotation=180)
            extrude(amount=6)
            fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[0], radius=2)
        super().__init__(p.part, rotation, align, mode)

class BaseSquare(BasePartObject):
    def __init__(self,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfilePlate()

            with Locations(
                    vertices().group_by(Axis.Z)[0].group_by(Axis.X)[0].
                    sort_by(Axis.Y)[0]):
                ScrewSupport(align=(Align.MIN, Align.MIN, Align.MIN))
                #fillet(edges(Select.NEW).filter_by(Axis.Z), radius=screw_support_fillet/3)
                
            with Locations(
                    vertices().group_by(Axis.Z)[0].group_by(Axis.X)[-1].
                    sort_by(Axis.Y)[-1]):
                ScrewSupport(align=(Align.MIN, Align.MIN, Align.MIN),
                        rotation=(0, 0, 180))
                #fillet(edges(Select.NEW).filter_by(Axis.Z), radius=screw_support_fillet/3)

            with Locations(faces().filter_by(Plane.YZ).sort_by(Axis.X)[0],
                        faces().filter_by(Plane.YZ).sort_by(Axis.X)[-1],
                        faces().filter_by(Plane.XZ).sort_by(Axis.Y)[0],
                        faces().filter_by(Plane.XZ).sort_by(Axis.Y)[-1]):
                with Locations(((plate_height + plate_base_height)/2, 0, 0)):
                    EdgeCut(edge_cut_len,
                            align=(Align.CENTER, Align.MAX, Align.CENTER),
                            rotation=(0, 0, -90),
                            mode=Mode.SUBTRACT)
        super().__init__(p.part, rotation, align, mode)

class BaseGrid(BasePartObject):
    def __init__(self, x, y,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            with GridLocations(bin_size, bin_size, x, y):
                BaseSquare()
            all_z_edges = edges().filter_by(Axis.Z)
            fillet(all_z_edges.group_by(Axis.X)[0].group_by(Axis.Y)[0] +
                   all_z_edges.group_by(Axis.X)[0].group_by(Axis.Y)[-1] +
                   all_z_edges.group_by(Axis.X)[-1].group_by(Axis.Y)[0] +
                   all_z_edges.group_by(Axis.X)[-1].group_by(Axis.Y)[-1],
                   radius=outer_rad)

        super().__init__(p.part, rotation, align, mode)

class ClipEdge(BasePartObject):
    def __init__(self, len,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            with BuildSketch(Plane.XZ):
                with BuildLine():
                    Polyline([(0, 0),
                              (1.2, 0),
                              (1.2, 1),
                              (1.4, 1),
                              (1.4, 1.2),
                              (1.2, 1.8),
                              (0, 1.8)],
                              close=True)
                make_face()
            extrude(amount=len)
            fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[1].
                   sort_by(Axis.X)[0], radius=0.18)
        
        super().__init__(p.part, rotation, align, mode)

