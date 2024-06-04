# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid

from gfthings.parameters import *
from gfthings.GFProfile import GFProfilePlate

class ScrewSupport(BasePartObject):
    def __init__(self,
                 magnet_rad : float = 3.1,
                 magnet_depth : float = 2,
                 screw_rad : float = 2,
                 counter_sink : bool = True,
                 margin : float = 2,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        screw_offset = 4.8
        margin = magnet_rad + margin

        with BuildPart() as p:
            len = screw_offset + margin
            # These were a bit too tall until I took 0.1mm off.
            height = plate_base_height - 0.1
            Box(len, len, height)
            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1]):
                offset = screw_offset - len/2
                with Locations((offset, offset)):
                    if counter_sink:
                        CounterSinkHole(screw_rad, magnet_rad)
                    else:
                        CounterBoreHole(screw_rad, magnet_rad, magnet_depth)
            minor_len = plate_height_a + plate_height_c
            with Locations((-len/2, -len/2)):
                Box(minor_len, len + margin, height,
                    align=(Align.MAX, Align.MIN, Align.CENTER))
                Box(len + margin, minor_len, height,
                    align=(Align.MIN, Align.MAX, Align.CENTER))
                Box(minor_len, minor_len, height,
                    align=(Align.MAX, Align.MAX, Align.CENTER))

            fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[-2].sort_by(Axis.X)[1],
                   radius=margin)
            fillet([edges().filter_by(Axis.Z).group_by(Axis.X)[-2].sort_by(Axis.Y)[0],
                    edges().filter_by(Axis.Z).group_by(Axis.Y)[-2].sort_by(Axis.X)[0]],
                   radius=len/4)

        super().__init__(p.part, rotation, align, mode)

class EdgeCut(BasePartObject):
    def __init__(self, cutout_long_len,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            import math
            # I'm not sure where the 0.05 fudge factor comes from but it seems to work.
            cutout_height = plate_height + 0.05
            tri_len = math.tan(30.0 * math.pi/180.0)*cutout_height
            cutout_short_len = cutout_long_len - tri_len*2
            with Locations((0, 0, -3)):
                with BuildSketch(Plane.XY):
                    Rectangle(cutout_short_len, cutout_height)
                    with Locations(
                            edges().filter_by(Axis.Y).sort_by(Axis.X)[0]@0.5):
                        Triangle(a=cutout_height, b=tri_len, C=90,
                                 align=(Align.CENTER, Align.MIN),
                                 rotation=90)
                    with Locations(
                            edges().filter_by(Axis.Y).sort_by(Axis.X)[-1]@0.5):
                        Triangle(a=tri_len, b=cutout_height, C=90,
                                 align=(Align.MAX, Align.CENTER),
                                 rotation=180)
            extrude(amount=6)
            fillet(edges().filter_by(Axis.Z).group_by(Axis.Y)[0], radius=2)
        super().__init__(p.part, rotation, align, mode)

class BaseSquare(BasePartObject):
    def __init__(self,
                 magnet_rad : float = 3.1,
                 magnet_depth : float = 2,
                 screw_rad : float = 2,
                 counter_sink : bool = False,
                 screw_hole_count : int = 2,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfilePlate()

            if screw_hole_count >= 2:
                with Locations(
                        vertices().group_by(Axis.Z)[0].group_by(Axis.X)[0].
                        sort_by(Axis.Y)[0]):
                    ScrewSupport(magnet_rad=magnet_rad,
                                magnet_depth=magnet_depth,
                                screw_rad=screw_rad,
                                counter_sink=counter_sink,
                                align=(Align.MIN, Align.MIN, Align.MIN))
                    
                with Locations(
                        vertices().group_by(Axis.Z)[0].group_by(Axis.X)[-1].
                        sort_by(Axis.Y)[-1]):
                    ScrewSupport(magnet_rad=magnet_rad,
                                magnet_depth=magnet_depth,
                                screw_rad=screw_rad,
                                counter_sink=counter_sink,
                                align=(Align.MIN, Align.MIN, Align.MIN),
                                rotation=(0, 0, 180))

            if screw_hole_count >= 4:
                with Locations(
                        vertices().group_by(Axis.Z)[0].group_by(Axis.X)[-1].
                        sort_by(Axis.Y)[0]):
                    ScrewSupport(magnet_rad=magnet_rad,
                                magnet_depth=magnet_depth,
                                screw_rad=screw_rad,
                                counter_sink=counter_sink,
                                align=(Align.MIN, Align.MIN, Align.MIN),
                                rotation=(0, 0, 90))
                with Locations(
                        vertices().group_by(Axis.Z)[0].group_by(Axis.X)[0].
                        sort_by(Axis.Y)[-1]):
                    ScrewSupport(magnet_rad=magnet_rad,
                                magnet_depth=magnet_depth,
                                screw_rad=screw_rad,
                                counter_sink=counter_sink,
                                align=(Align.MIN, Align.MIN, Align.MIN),
                                rotation=(0, 0, 270))

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
    def __init__(self, x_num, y_num,
                 magnet_rad : float = 3.1,
                 magnet_depth : float = 2,
                 screw_rad : float = 2,
                 counter_sink : bool = False,
                 screw_hole_count : int = 2,
                 screw_hole_pattern_drawer : bool = False,
                 corner_screw_hole_count : int = 0,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            with GridLocations(bin_size, bin_size, x_num, y_num):
                BaseSquare(magnet_rad=magnet_rad,
                    magnet_depth=magnet_depth,
                    screw_rad=screw_rad,
                    screw_hole_count=screw_hole_count,
                    counter_sink=counter_sink)

            if screw_hole_pattern_drawer and x_num > 2 and y_num > 2:
                with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[0].center()):
                    with Locations((-(bin_size * x_num)/2+bin_size, 
                                    -(bin_size * y_num)/2+bin_size, 
                                    0)):
                        ScrewSupport(magnet_rad=magnet_rad,
                                    magnet_depth=magnet_depth,
                                    screw_rad=screw_rad,
                                    counter_sink=counter_sink,
                                    align=(Align.MIN, Align.MIN, Align.MIN))
                    with Locations((-(bin_size * x_num)/2+bin_size,
                                    (bin_size * y_num)/2-bin_size,
                                    0)):
                        ScrewSupport(magnet_rad=magnet_rad,
                                    magnet_depth=magnet_depth,
                                    screw_rad=screw_rad,
                                    counter_sink=counter_sink,
                                    rotation=(0, 0, 270),
                                    align=(Align.MIN, Align.MIN, Align.MIN))
                    with Locations(((bin_size * x_num)/2-bin_size,
                                    (bin_size * y_num)/2-bin_size,
                                    0)):
                        ScrewSupport(magnet_rad=magnet_rad,
                                    magnet_depth=magnet_depth,
                                    screw_rad=screw_rad,
                                    counter_sink=counter_sink,
                                    rotation=(0, 0, 180),
                                    align=(Align.MIN, Align.MIN, Align.MIN))
                    with Locations(((bin_size * x_num)/2-bin_size,
                                    -(bin_size * y_num)/2+bin_size,
                                    0)):
                        ScrewSupport(magnet_rad=magnet_rad,
                                    magnet_depth=magnet_depth,
                                    screw_rad=screw_rad,
                                    counter_sink=counter_sink,
                                    rotation=(0, 0, 90),
                                    align=(Align.MIN, Align.MIN, Align.MIN))

            all_z_edges = edges().filter_by(Axis.Z)
            fillet(all_z_edges.group_by(Axis.X)[0].group_by(Axis.Y)[0] +
                   all_z_edges.group_by(Axis.X)[0].group_by(Axis.Y)[-1] +
                   all_z_edges.group_by(Axis.X)[-1].group_by(Axis.Y)[0] +
                   all_z_edges.group_by(Axis.X)[-1].group_by(Axis.Y)[-1],
                   radius=outer_rad)

            clip_edge_height = -(plate_height + plate_base_height)/2 + 4.7
            with Locations((-(bin_size * x_num)/2, 0, clip_edge_height)):
                with GridLocations(bin_size, bin_size, 1, y_num):
                    ClipEdge(edge_cut_len,
                             rotation=(0, 0, 0),
                             align=(Align.MIN, Align.CENTER, Align.MAX))
            with Locations(((bin_size*x_num)/2, 0, clip_edge_height)):
                with GridLocations(bin_size, bin_size, 1, y_num):
                    ClipEdge(edge_cut_len,
                             rotation=(0, 0, 180),
                             align=(Align.MIN, Align.CENTER, Align.MAX))
            with Locations((0, -(bin_size*y_num)/2, clip_edge_height)):
                with GridLocations(bin_size, bin_size, x_num, 1):
                    ClipEdge(edge_cut_len,
                             rotation=(0, 0, 90),
                             align=(Align.MIN, Align.CENTER, Align.MAX))
            with Locations((0, (bin_size*y_num)/2, clip_edge_height)):
                with GridLocations(bin_size, bin_size, x_num, 1):
                    ClipEdge(edge_cut_len,
                             rotation=(0, 0, 270),
                             align=(Align.MIN, Align.CENTER, Align.MAX))

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

if __name__ == "__main__":
    from ocp_vscode import show_object, set_port
    set_port(3939)

    show_object(BaseGrid(4, 4, 
                         screw_hole_count=0,
                         screw_hole_pattern_drawer=True),
                "Test")
    