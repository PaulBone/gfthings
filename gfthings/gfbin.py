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
    parser.add_argument(
        "--unrefined",
        help="Use unrefined magnet holes. " +
            "Gridfinity Refind " + 
            "https://www.printables.com/model/413761-gridfinity-refined " +
            "has improved magnet holes that don't require glue, " +
            "If for some reason you don't want superiour magnet holes then " +
            "--unrefind will switch to plain circular holes",
        action="store_true")
    parser.add_argument(
        "--magnet-dia",
        help="Magnet hole diameter or width for 'refined' holes. " +
             "(default %(default)s)",
        type=float,
        default=6)
    parser.add_argument(
        "--magnet-height",
        help="Height of refind magnet slots / " + 
             "depth of traditional magnet holes. " +
             "(default %(default)s)",
        type=float,
        default=2)
    
    args = parser.parse_args(argv)
    x = int(args.x)
    y = int(args.y)
    z = int(args.z)
    scoop = float(args.scoop)
    divisions = int(args.divisions)

    bin = Bin(x, y, z, scoop,
              divisions=divisions,
              label=not args.no_label,
              refined=not args.unrefined,
              magnet_dia=args.magnet_dia,
              magnet_depth=args.magnet_height)
    
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
