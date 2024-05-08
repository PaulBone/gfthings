from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from parameters import *
from GFProfile import GFProfileBin, GFProfileLip

magnet_depth=2.2

class BinBase(BasePartObject):
    def __init__(self, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfileBin()
            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[0]):
                magnet_offset = 35.6/2 - 4.8
                with GridLocations(magnet_offset*2, magnet_offset*2, 2, 2):
                    Hole(magnet_dia/2, magnet_depth)                
            
        super().__init__(p.part, rotation, align, mode)

class Scoop(BasePartObject):
    def __init__(self, rad : float, len : float, height : float, wall_thickness : float, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        wall_pad = plate_height_a + plate_height_c - wall_thickness
        with BuildPart() as p:
            with BuildSketch(Plane.YZ):
                Rectangle(rad, rad)
                with Locations((rad/2, rad/2)):
                    Circle(rad, rad, mode=Mode.SUBTRACT)
            extrude(amount=len)
            with Locations(edges().filter_by(Axis.X).group_by(Axis.Y)[0].sort_by(Axis.Z)[0]@0.5):
                Box(len, wall_pad, height, align=(Align.CENTER, Align.MAX, Align.MIN))

        super().__init__(p.part, rotation, align, mode)

class BinLip(BasePartObject):
    def __init__(self, width : int, depth : int, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfileLip(width, depth, support=60, base=0.8)

        super().__init__(p.part, rotation, align, mode)

class Bin(BasePartObject):
    def __init__(self, width : int, depth : int, height_units : int, scoop_rad : float, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        height = 7 * height_units
        bin_clearance = 0.5
        wall_thickness = 1.2
        with BuildPart() as p:
            wall_height = height - plate_height
            
            Box(width * bin_size - bin_clearance * 2,
                depth * bin_size - bin_clearance * 2,
                wall_height)
            fillet(edges().filter_by(Axis.Z), radius=outer_rad)
            with Locations((0, 0, -wall_height/2)):
                with GridLocations(bin_size, bin_size, width, depth):
                    BinBase(align=(Align.CENTER, Align.CENTER, Align.MAX))
            
            inner_width = width * bin_size - bin_clearance*2 - wall_thickness*2
            inner_depth = depth * bin_size - bin_clearance*2 - wall_thickness*2
            with BuildSketch(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1]):
                RectangleRounded(inner_width, inner_depth,
                                 radius=outer_rad - bin_clearance - wall_thickness)
            inner_height = wall_height - wall_thickness
            extrude(amount=-inner_height, mode=Mode.SUBTRACT)

            if scoop_rad and scoop_rad > 0:
                with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-2].edges().filter_by(Axis.X).sort_by(Axis.Y)[0]@0.5):
                    Scoop(scoop_rad, inner_width, inner_height, wall_thickness, align=(Align.CENTER, Align.MIN, Align.MIN)) 

            with Locations((0, 0, wall_height/2 + plate_height)):
                BinLip(width, depth, align=(Align.CENTER, Align.CENTER, Align.MAX))
            
        super().__init__(p.part, rotation, align, mode)

show_object(Bin(2, 1, 3, 12), "test")
