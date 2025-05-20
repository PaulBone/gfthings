# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

import gfthings.Base as Base
from Utils import float_eq

def test_2x2_base():
    base = Base.BaseGrid(2, 2,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=2,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(9425.715783704205, base.volume)

def test_1x1_base():
    base = Base.BaseGrid(1, 1,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=2,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(2384.7658445843413, base.volume)
    
def test_4_holes():
    base = Base.BaseGrid(2, 2,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=4,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(10986.224490884395, base.volume)

def test_big_base():
    base = Base.BaseGrid(5, 5,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=0,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(48185.65844308989, base.volume)

def test_big_drawer_base():
    base = Base.BaseGrid(5, 5,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=0,
                         screw_hole_pattern_drawer=True,
                         corner_screw_hole_count=0)
    float_eq(48965.91279674202, base.volume)

def test_screw_holes():
    base = Base.BaseGrid(2, 2,
                         magnet_rad=3.1,
                         magnet_depth=1,
                         screw_rad=2,
                         counter_sink=True,
                         screw_hole_count=2,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(9624.911063054498, base.volume)
