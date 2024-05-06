
from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid
from ocp_vscode import show, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from parameters import *

class GFProfile(BasePartObject):
    def __init__(self, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        with BuildPart() as p:
            with BuildSketch():
                RectangleRounded(bin_size, bin_size, radius=outer_rad)
            extrude(amount=plate_height)
            
            with BuildLine(mode=Mode.PRIVATE):
                b = bin_size/2
                path = FilletPolyline((-b, -b), (-b, b), (b, b), (b, -b),
                                    radius=outer_rad, close=True)
                
            with BuildSketch(Plane(origin=path@0, z_dir=path%0).rotated((-90, 0, 0))):
                with BuildLine():
                        Polyline(
                            (0, 0),
                            (0, plate_height),
                            (-plate_height_c, plate_height_a + plate_height_b + plate_base_height),
                            (-plate_height_c, plate_height_a + plate_base_height),
                            (-plate_height_a - plate_height_c, plate_base_height),
                            (-plate_height_a - plate_height_c, 0),
                            close=True)
                make_face()
            sweep(path=path, mode=Mode.SUBTRACT)

        super().__init__(part=p.part, rotation=rotation, align=align, mode=mode)
