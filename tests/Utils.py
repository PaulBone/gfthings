# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

import sys
from pathlib import Path

# This finds the absolute path to the 'src' directory relative to this file
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path) 

print(sys.path)

# Comparing floating-point numbers should always be done with some error
# margin.
def float_eq(exp, got):
    epsilon = 0.001
    assert got < exp + epsilon
    assert got > exp - epsilon
