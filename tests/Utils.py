# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

# Comparing floating-point numbers should always be done with some error
# margin.
def float_eq(exp, got):
    epsilon = 0.001
    assert got < exp + epsilon
    assert got > exp - epsilon
