
from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid
from ocp_vscode import show, reset_show, set_port, set_defaults, get_defaults, show_object
set_port(3939)

from parameters import *

class GFProfile(BasePartObject):
    def __init__(self, base = True, rotation: tuple[float, float, float] | Rotation = (0, 0, 0), align: Align | tuple[Align, Align, Align] = None, mode: Mode = Mode.ADD):
        my_bin_size = bin_size
        my_outer_rad = outer_rad
        if not base:
             my_bin_size = 41.5
             my_outer_rad = 7.5/2
        with BuildPart() as p:
            with BuildSketch():
                RectangleRounded(my_bin_size, my_bin_size, radius=my_outer_rad)
            extrude(amount=plate_height)
            
            with BuildLine(mode=Mode.PRIVATE):
                b = my_bin_size/2
                path = FilletPolyline((-b, -b), (-b, b), (b, b), (b, -b),
                                    radius=my_outer_rad, close=True)
                
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

            if not base:
                Box(bin_size, bin_size, plate_base_height, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))

        super().__init__(part=p.part, rotation=rotation, align=align, mode=mode)

if (__name__ == "__main__"):
    show_object(GFProfile(), "plate")
    show_object(GFProfile(False), "bin")
