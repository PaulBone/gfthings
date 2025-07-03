
# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from gfthings.Edge import Edge
from Utils import float_eq

def test_simple_edge():
    edge = Edge(1, 21)
    float_eq(1136.9891783849928, edge.volume)

def test_long_edge():
    edge = Edge(4, 21)
    float_eq(4547.956713539974, edge.volume)

def test_narrow_edge():
    edge = Edge(2, 12)
    float_eq(1957.3276090903773, edge.volume)

def test_short_edge():
    edge = Edge(2, 12, short=True)
    float_eq(1040.5549203673213, edge.volume)