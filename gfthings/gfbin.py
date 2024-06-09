# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from argparse import ArgumentParser
from build123d import *

from gfthings.Bin import Bin

def main(argv: list[str] | None = None):
    parser = ArgumentParser(
            description="Generate a Gridfinity bin")
    parser.add_argument(
        "--vscode",
        help="Run in vscode_ocp mode and connect to the given port. " +
             "Do not produce a .step file.",
        default=0)
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename (default: %(default)s)",
        default="bin.step")
    parser.add_argument(
        "-x",
        help="Width of the bin in gridfinity units (default: %(default)s)",
        default=1)
    parser.add_argument(
        "-y",
        help="Depth of the bin in gridfinity units (default: %(default)s)",
        default=1)
    parser.add_argument(
        "-z",
        help="Height of the bin in gridfinity units, must be at least 3 (default: %(default)s)",
        default=4)
    parser.add_argument(
        "-s",
        "--scoop",
        help="Radius of the scoop at the front, " +
            "in millimeters, 0 to disable " +
            "(default %(default)s)",
        default=12.5)
    parser.add_argument(
        "-d",
        "--divisions",
        help="Number of divisions. " +
            "2 means that 1 wall will divide the bin into 2 parts. " +
            "3 or more divisions per gridfinity unit is not recommended " +
            "as the pockets become too small to fit my finger in. " +
            "(default %(default)s)",
        default=1)
    parser.add_argument(
        "--no-label",
        help="Don't add a shelf for the label",
        action="store_true")
        
    args = parser.parse_args(argv)
    x = int(args.x)
    y = int(args.y)
    z = int(args.z)
    scoop = float(args.scoop)
    divisions = int(args.divisions)

    bin = Bin(x, y, z, scoop, divisions=divisions, label=not args.no_label)
    
    if args.vscode:
        from ocp_vscode import (show_object,
                                set_port)
        set_port(args.vscode)
        show_object(bin, "bin")
    else:
        export_step(bin, args.output)
        
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
