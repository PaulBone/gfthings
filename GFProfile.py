
from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid
from ocp_vscode import show, reset_show, set_port, set_defaults, get_defaults, show_object
set_port(3939)

from parameters import *

class GFProfile(BasePartObject):
    def __init__(self, width : int = 1,
                       depth : int = 1,
                       bin_size : float = 42,
                       clearance : float = 0,
                       corner_dia : float = 8,
                       base : float = 0,
                       support : float = 0,
                       rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                       align: Align | tuple[Align, Align, Align] = None,
                       mode: Mode = Mode.ADD):
        with BuildPart() as p:
            with BuildSketch():
                RectangleRounded(bin_size * width - clearance * 2,
                                 bin_size * depth - clearance * 2,
                                 radius=corner_dia/2)
            extrude(amount=plate_height + base + support)
            
            with BuildLine(mode=Mode.PRIVATE):
                w = width*bin_size/2 - clearance
                d = depth*bin_size/2 - clearance
                path = FilletPolyline((-w, -d), (-w, d), (w, d), (w, -d),
                                      radius=corner_dia/2, close=True)
            
            # build123d can't handle a line with no length.
            if base == 0:
                base = 0.01
            with BuildSketch(Plane(origin=path@0, z_dir=path%0).rotated((-90, 0, 0))):
                with BuildLine():
                        Polyline(
                            (0, support),
                            (0, support + plate_height + base),
                            (-plate_height_c, support + plate_height_a + plate_height_b + base),
                            (-plate_height_c, support + plate_height_a + base),
                            (-plate_height_a - plate_height_c, support + base),
                            (-plate_height_a - plate_height_c, support),
                            (0, 0),
                            close=True)
                        
                make_face()
            sweep(path=path, mode=Mode.SUBTRACT)
        super().__init__(part=p.part, rotation=rotation, align=align, mode=mode)

class GFProfilePlate(BasePartObject):
    def __init__(self, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        with BuildPart() as p:
            Box(bin_size, bin_size, plate_height + plate_base_height)
            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1].center()):
                GFProfile(base=plate_base_height, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MAX))                
            
        super().__init__(p.part, rotation, align, mode)

class GFProfileBin(BasePartObject):
    def __init__(self, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfile(bin_size=41.5, corner_dia=7.5)
        super().__init__(p.part, rotation, align, mode)

class GFProfileLip(BasePartObject):
    def __init__(self, width : int = 1, depth : int = 1, support : float = 60, base : float = 0.8, 
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        size = 42
        clearance = 0.5
        dia = 7.5
        import math
        support_height = math.tan(support*math.pi/180.0) / (plate_height_a + plate_height_c)
        with BuildPart() as p:
            with BuildSketch(Plane.XY):
                RectangleRounded(width * size - clearance*2, depth * size - clearance*2, radius=dia/2)
            extrude(amount=plate_height + support_height + base)

            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1]):
                GFProfile(width, depth, bin_size=42,
                          clearance=clearance,
                          corner_dia=7.5,
                          support=support_height,
                          base=0.8,
                          mode=Mode.SUBTRACT,
                          align=(Align.CENTER, Align.CENTER, Align.MAX))
        super().__init__(p.part, rotation, align, mode)

if (__name__ == "__main__"):
    show_object(GFProfilePlate(), "plate")
    show_object(GFProfileBin(), "bin")
    show_object(GFProfileLip(1, 1, support=60), "lip")
