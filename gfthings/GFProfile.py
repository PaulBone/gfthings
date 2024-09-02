# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid

from gfthings.parameters import *

class GFProfile(BasePartObject):
    def __init__(self, width : float = 1,
                       depth : float = 1,
                       clearance : float = 0,
                       corner_dia : float = base_outer_dia,
                       base : float = 0,
                       support : float = 0,
                       inner_clearance : float = 0,
                       rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                       align: Align | tuple[Align, Align, Align] = None,
                       mode: Mode = Mode.ADD):
        with BuildPart() as p:
            with BuildSketch():
                RectangleRounded(width * bin_size - clearance * 2,
                                 depth * bin_size - clearance * 2,
                                 radius=corner_dia/2)
            extrude(amount=plate_height + base + support - inner_clearance)
            
            with BuildLine(mode=Mode.PRIVATE):
                w = width * bin_size/2 - clearance
                d = depth * bin_size/2 - clearance
                path = FilletPolyline((-w, -d), (-w, d), (w, d), (w, -d),
                                      radius=corner_dia/2, close=True)
            
            # build123d can't handle a line with no length.
            if base == 0:
                base = 0.01
            with BuildSketch(Plane(origin=path@0, z_dir=path%0).rotated((-90, 0, 0))):
                with BuildLine():
                        Polyline(
                            (0, support),
                            (0, support + plate_height + base - inner_clearance),
                            (-plate_height_c, support + plate_height_a - inner_clearance + plate_height_b + base),
                            (-plate_height_c, support + plate_height_a - inner_clearance + base),
                            (-plate_height_a + inner_clearance - plate_height_c, support + base),
                            (-plate_height_a + inner_clearance - plate_height_c, support),
                            (0, 0),
                            close=True)
                        
                make_face()
            sweep(path=path, mode=Mode.SUBTRACT)
        super().__init__(part=p.part, rotation=rotation, align=align, mode=mode)

class GFProfilePlate(BasePartObject):
    def __init__(self, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        with BuildPart() as p:
            Box(bin_size, bin_size, plate_height + plate_base_height - 0.1)
            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1].center()):
                GFProfile(clearance=0, inner_clearance=0, base=plate_base_height, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MAX))
            
        super().__init__(p.part, rotation, align, mode)

class GFProfileBin(BasePartObject):
    def __init__(self, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfile(clearance=0.25, inner_clearance=0, corner_dia=7.5)
        super().__init__(p.part, rotation, align, mode)

class GFProfileLip(BasePartObject):
    def __init__(self, width : int = 1, depth : int = 1, support : float = 45, base : float = 0.8, shelf_clearance : float = 0.1,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        import math
        support_height = (plate_height_a + plate_height_c) / math.tan(support*math.pi/180.0)
        with BuildPart() as p:
            with BuildSketch(Plane.XY):
                RectangleRounded(width * bin_size - bin_clearance*2,
                                 depth * bin_size - bin_clearance*2,
                                 radius=outer_rad)
            extrude(amount=plate_height + support_height + base - shelf_clearance)

            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1]):
                GFProfile(width=width,
                          depth=depth,
                          clearance=0,
                          corner_dia=outer_rad*2,
                          support=support_height,
                          base=base,
                          inner_clearance=0.1,
                          mode=Mode.SUBTRACT,
                          align=(Align.CENTER, Align.CENTER, Align.MAX))
        super().__init__(p.part, rotation, align, mode)

if (__name__ == "__main__"):
    from ocp_vscode import show, reset_show, set_port, set_defaults, get_defaults, show_object
    set_port(3939)

    show_object(GFProfilePlate(), "plate", measure_tools=True)
    show_object(GFProfileBin(), "bin", measure_tools=True)
    show_object(GFProfileLip(1, 2, support=60), "lip", measure_tools=True)
