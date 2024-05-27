# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from build123d import *
from build123d.build_enums import Align, Mode
from build123d.topology import Part, Solid

from gfthings.parameters import *
from gfthings.GFProfile import GFProfileBin, GFProfileLip

magnet_depth=2.2

class BinBase(BasePartObject):
    def __init__(self,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfileBin()
            with Locations(faces().filter_by(Plane.XY).sort_by(Axis.Z)[0]):
                magnet_offset = 35.6/2 - 4.8
                with GridLocations(magnet_offset*2, magnet_offset*2, 2, 2):
                    Hole(magnet_dia/2, magnet_depth)                
            
        super().__init__(p.part, rotation, align, mode)

class Scoop(BasePartObject):
    def __init__(self, rad : float, len : float, height : float,
                 wall_thickness : float,
                 shelf_clearance : float,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        wall_pad = plate_height_a + plate_height_c - wall_thickness - \
                shelf_clearance
        with BuildPart() as p:
            with BuildSketch(Plane.YZ):
                Rectangle(rad, rad)
                with Locations((rad/2, rad/2)):
                    Circle(rad, rad, mode=Mode.SUBTRACT)
            extrude(amount=len)
            with Locations(edges().filter_by(Axis.X).group_by(Axis.Y)[0]
                    .sort_by(Axis.Z)[0]@0.5):
                Box(len, wall_pad, height,
                    align=(Align.CENTER, Align.MAX, Align.MIN))

        super().__init__(p.part, rotation, align, mode)

class BinLip(BasePartObject):
    def __init__(self, width : int, depth : int, shelf_clearance : float,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        with BuildPart() as p:
            GFProfileLip(width, depth, support=45,
                         base=0.8, shelf_clearance=shelf_clearance)

        super().__init__(p.part, rotation, align, mode)

class LabelShelf(BasePartObject):
    def __init__(self, len : float,
                 shelf_clearance : float,
                 shelf_overhang_angle : float = 60,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        shelf_depth=12
        edge_depth=1.2
        shelf_height = 2
        lip_height_c = 1.9
        lip_height_a = 0.7
        depth_from_wall = lip_height_a + lip_height_c - wall_thickness
        depth = shelf_depth + edge_depth + depth_from_wall
        inner_height = 1
        with BuildPart() as p:
            Box(len, depth, shelf_height)
            with BuildSketch(Plane(faces().filter_by(Plane.XY)
                    .sort_by(Axis.Z)[-1])):
                with Locations((0, depth/2 - depth_from_wall)):
                    RectangleRounded(len - depth_from_wall*2, shelf_depth,
                                     outer_rad - plate_height_a +
                                         shelf_clearance - plate_height_c,
                                     align=(Align.CENTER, Align.MAX))
            extrude(amount=-inner_height, mode=Mode.SUBTRACT)
            fillet(edges().filter_by(Axis.X).group_by(Axis.Y)[0]
                        .group_by(Axis.Z)[-1],
                   radius=min(shelf_height, edge_depth*0.75))
            
            if shelf_overhang_angle < 90:
                import math
                support_height = depth / \
                        math.tan(shelf_overhang_angle * math.pi / 180.0)
                with BuildSketch(Plane(
                        origin=edges().filter_by(Axis.Y).group_by(Axis.Z)[0]
                            .sort_by(Axis.X)[0]@1,
                        x_dir=(0, 1, 0),
                        z_dir=(1, 0, 0))):
                    with BuildLine():
                        Polyline((0, 0),
                                 (0, -support_height),
                                 (-depth, 0),
                                 close=True)
                    make_face()
                extrude(amount=len)
            
        super().__init__(p.part, rotation, align, mode)

class Bin(BasePartObject):
    def __init__(self, width : int, depth : int,
                 height_units : int,
                 scoop_rad : float,
                 divisions : int = 1,
                 rotation: tuple[float, float, float] | Rotation = (0, 0, 0),
                 align: Align | tuple[Align, Align, Align] = None,
                 mode: Mode = Mode.ADD):
        height = 7 * height_units
        shelf_clearance = 0.1
        with BuildPart() as p:
            wall_height = height - plate_height
            box_width = width * bin_size - bin_clearance * 2
            box_depth = depth * bin_size - bin_clearance * 2
            Box(box_width, box_depth, wall_height)
            fillet(edges().filter_by(Axis.Z), radius=outer_rad)
            with Locations((0, 0, -wall_height/2)):
                with GridLocations(bin_size, bin_size, width, depth):
                    BinBase(align=(Align.CENTER, Align.CENTER, Align.MAX))
            
            inner_width = width * bin_size - bin_clearance*2 - wall_thickness*2
            inner_depth = depth * bin_size - bin_clearance*2 - wall_thickness*2
            with BuildSketch(faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1]):
                RectangleRounded(inner_width, inner_depth,
                                 radius=outer_rad - bin_clearance -
                                    wall_thickness)
            inner_height = wall_height - wall_thickness
            extrude(amount=-inner_height, mode=Mode.SUBTRACT)

            inner_front_centre = faces().filter_by(Plane.XY) \
                .sort_by(Axis.Z)[-2].edges().filter_by(Axis.X) \
                .sort_by(Axis.Y)[0]@0.5
            if divisions > 1:
                dividors = divisions-1
                dividor_space = inner_width / divisions
                with Locations(inner_front_centre):
                    with GridLocations(dividor_space, 1, dividors, 1):
                        # Use inner_height if there's no shelf, otherwise
                        # subtract the shelf's cuttout depth.
                        Box(wall_thickness, inner_depth, inner_height - 1.1,
                            align=(Align.CENTER, Align.MIN, Align.MIN))

            if scoop_rad and scoop_rad > 0:
                with Locations(inner_front_centre):
                    Scoop(scoop_rad, inner_width, inner_height,
                          wall_thickness, shelf_clearance,
                          align=(Align.CENTER, Align.MIN, Align.MIN)) 

            with Locations((0, 0, wall_height/2 + plate_height)):
                BinLip(width, depth, shelf_clearance=shelf_clearance,
                       align=(Align.CENTER, Align.CENTER, Align.MAX))
            
            with Locations(Plane(origin=faces().filter_by(Plane.XZ)
                    .sort_by(Axis.Y)[-1].edges().filter_by(Axis.X)
                    .sort_by(Axis.Z)[-1]@0.5)):
                with Locations((0, -wall_thickness, -plate_height)):
                    LabelShelf(box_width - 2*wall_thickness, shelf_clearance,
                               align=(Align.CENTER, Align.MAX, Align.MAX))
                    # Cut out parts for the label to fit under.
                    with Locations((0, -label_depth/2 - plate_height_a -
                            plate_height_c + wall_thickness, 0)):
                        Box(box_width - 2*wall_thickness, label_tab_depth, 1,
                            align=(Align.CENTER, Align.CENTER, Align.MAX),
                            mode=Mode.SUBTRACT)
            
            # Round off the top edge because it's too sharp for 3D printing.
            with Locations(bounding_box().faces().filter_by(Plane.XY)
                    .sort_by(Axis.Z)[-1].center()):
                Box(box_width, box_depth, 0.3,
                    align=(Align.CENTER, Align.CENTER, Align.MAX),
                    mode=Mode.SUBTRACT)
            

        super().__init__(p.part, rotation, align, mode)
