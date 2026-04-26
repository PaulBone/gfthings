# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

# Comparing floating-point numbers should always be done with some error
# margin. The tolerance accommodates small variance between build123d
# versions (notably between the released 0.10.0 and the upstream `dev`
# branch used on Python 3.14); OCCT boolean operations can shift volumes
# by ~0.05 mm^3 between versions for the same input geometry.
def float_eq(exp, got):
    epsilon = 0.05
    assert got < exp + epsilon
    assert got > exp - epsilon
