# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

import gfthings.Bin as Bin

from Utils import float_eq

def test_simple_bin():
    bin = Bin.Bin(1, 1, 4, scoop_rad=0, divisions=1, label=False)
    float_eq(12291.10855478232, bin.volume)

def test_1x2_bin():
    bin1 = Bin.Bin(1, 2, 4, scoop_rad=0, divisions=1, label=False)
    float_eq(25675.874203463918, bin1.volume)

    # bin2 should be symetrical.
    bin2 = Bin.Bin(2, 1, 4, scoop_rad=0, divisions=1, label=False)
    float_eq(bin2.volume, bin1.volume)

def test_3x3_bin():
    bin = Bin.Bin(3, 3, 4, scoop_rad=0, divisions=1, label=False)
    float_eq(94178.78960458007, bin.volume)

def test_tall_bin():
    bin = Bin.Bin(1, 1, 6, scoop_rad=0, divisions=1, label=False)
    float_eq(14893.843256865446, bin.volume)

def test_bin_shelf():
    bin = Bin.Bin(1, 1, 4, scoop_rad=0, divisions=1, label=True)
    float_eq(15245.41393395344, bin.volume)

def test_divided_bin():
    bin = Bin.Bin(2, 1, 4, scoop_rad=0, divisions=2, label=False)
    float_eq(26654.758787176816, bin.volume)

def test_scoop():
    bin1 = Bin.Bin(1, 1, 5, scoop_rad=8, divisions=1, label=False)
    float_eq(15576.908255536231, bin1.volume)
    bin2 = Bin.Bin(1, 1, 5, scoop_rad=12, divisions=1, label=False)
    float_eq(16237.95684535477, bin2.volume)

def test_half():
    bin = Bin.Bin(1, 1, 4, scoop_rad=0, divisions=1, label=False,
                  half_grid=True)
    float_eq(13252.86144442649, bin.volume)
    bin = Bin.Bin(1.5, 1, 4, scoop_rad=0, divisions=1, label=False,
                  half_grid=True)
    float_eq(18596.997883502943, bin.volume)
    
