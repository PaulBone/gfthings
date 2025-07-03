# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

import sys
sys.path.append("gfthings/")

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
    float_eq(9423.834706464077, base.volume)

def test_2x2_short_base():
    base = Base.BaseGrid(2, 2,
                         screw_hole_count=0,
                         short=True)
    float_eq(4010.0901306660126, base.volume)

def test_1x1_base():
    base = Base.BaseGrid(1, 1,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=2,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(2383.825305964295, base.volume)

def test_1x1_short_base():
    base = Base.BaseGrid(1, 1,
                         screw_hole_count=0,
                         short=True)
    float_eq(1049.4015434827163, base.volume)
    
def test_4_holes():
    base = Base.BaseGrid(2, 2,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=4,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(10984.343413653465, base.volume)

def test_big_base():
    base = Base.BaseGrid(5, 5,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=0,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(48180.955749932196, base.volume)

def test_big_drawer_base():
    base = Base.BaseGrid(5, 5,
                         magnet_rad=3.1,
                         magnet_depth=2,
                         screw_rad=2,
                         counter_sink=False,
                         screw_hole_count=0,
                         screw_hole_pattern_drawer=True,
                         corner_screw_hole_count=0)
    float_eq(48961.210103592195, base.volume)

def test_screw_holes():
    base = Base.BaseGrid(2, 2,
                         magnet_rad=3.1,
                         magnet_depth=1,
                         screw_rad=2,
                         counter_sink=True,
                         screw_hole_count=2,
                         screw_hole_pattern_drawer=False,
                         corner_screw_hole_count=0)
    float_eq(9623.029985813218, base.volume)
