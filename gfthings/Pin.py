
from build123d import *
from build123d.build_enums import Align, Mode
import math

from build123d.topology import Part, Solid

from .parameters import *

class Pin(BasePartObject):
    def __init__(self, 
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            # `plate_base_height` was originally a constant (2.9) and became
            # a function `(short: bool) -> float` when --short bases were
            # added (build123d commit e7296b9). Pin was not migrated at the
            # time, so `3.2 + plate_base_height + 0.5` raised
            # `TypeError: unsupported operand type(s) for +: 'float' and
            # 'function'` on every invocation of `gfpin`. Pins are physical
            # parts independent of base height and the original code targeted
            # the 2.9mm (non-short) base, so we explicitly pass False here to
            # preserve the historical geometry.
            total_height = 3.2 + plate_base_height(False) + 0.5
            shaft_len = total_height - (magnet_dia - screw_dia)/2
            inner_shaft = 1.0
            outer_shaft = 1.7
            peg_rad = 0.5
            cut_width = 0.8
            
            with BuildSketch(Plane.XZ):
                with BuildLine() as f:
                    
                    Polyline((inner_shaft, -(outer_shaft - inner_shaft)),
                            (outer_shaft + peg_rad, peg_rad), 
                            (outer_shaft, peg_rad + math.tan(20*math.pi/180)*peg_rad),
                            (outer_shaft, peg_rad + shaft_len),
                            (magnet_dia/2-0.2, peg_rad + total_height),
                            (0, peg_rad + total_height),
                            (0, peg_rad + shaft_len),
                            (inner_shaft, peg_rad + shaft_len),
                            (inner_shaft, -(outer_shaft - inner_shaft)))
                make_face()
            revolve()
            with Locations((0, 0, -(peg_rad + (outer_shaft - inner_shaft)))):
                cut_len = 3*shaft_len/4 + peg_rad + (outer_shaft - inner_shaft)
                Box(50, cut_width, cut_len, 
                    mode=Mode.SUBTRACT,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
                Box(cut_width, 50, cut_len,
                    mode=Mode.SUBTRACT,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))

        super().__init__(p.part, rotation, align, mode)
