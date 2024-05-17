
Paul's Gridfinity Things
========================

This Python program will generate several different kinds of gridfinity
compatible objects for 3D printing

Setup, you need the build123d python library, which is installed with
poetry, poetry is installed with pipx (or maybe with apt, I haven't tried),
pipx is installed with apt, and apt is installed with Debian or Ubuntu
Linux.

    sudo apt install pipx
    pipx install poetry
    poetry install

Copyright (C) Paul Bone
Distributed under: CC BY-NC-SA 4.0
https://creativecommons.org/licenses/by-nc-sa/4.0/


Bins
----

TODO.


Pins
----

Pins, or pegs, are a small object that can be used to attach a Gridfinity
base to a sheet of plywood such as found in the bottom of many desk drawers.
Run:

    poetry run gfpin

To generate pin.step.  Print it at a higher temperature if you can for
strong layer adheasion.  Pressing it through the gridfinity base and a 3mm
driled hole can take some force.  I don't know how easy it is to remove -
the question hasn't come up!



