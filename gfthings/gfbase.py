# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from argparse import ArgumentParser
from build123d import *

from gfthings.parameters import *
from gfthings.Base import *

def main(argv: list[str] | None = None):
    parser = ArgumentParser(
            description="Generate a Gridfinity base")
    parser.add_argument(
        "--vscode",
        help="Run in vscode_ocp mode and connect to the given port. " +
             "Do not produce a .step file.",
        default=0)
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename, defaults to %(default)s",
        default="base.step")
    parser.add_argument(
        "-x",
        help="Number of squares across (default: %(default)s",
        default=4)
    parser.add_argument(
        "-y",
        help="Number of squares deep (default: %(default)s",
        default=4)
    parser.add_argument(
        "--screw-diameter",
        help="Diameter for screw holes (default: %(default)s",
        default=4,
        type=float)
    parser.add_argument(
        "--magnet-diameter",
        help="Diameter for magnet holes or countersink diameter (default: %(default)s",
        default=6.2,
        type=float)
    parser.add_argument(
        "--magnet-depth",
        help="Depth of magnet hole (default %(default)s",
        default=2,
        type=float)
    # I haven't tested prints with these yet.
    #parser.add_argument(
    #    "--countersink",
    #    help="Countersink the screw holes rather than counterbore",
    #    action="store_true")
    
    args = parser.parse_args(argv)

    x = int(args.x)
    y = int(args.y)
    screw_rad = args.screw_diameter/2
    magnet_rad = args.magnet_diameter/2
    magnet_depth = args.magnet_depth
    #counter_sink = bool(args.countersink)
    counter_sink = False
    base = BaseGrid(x, y,
                    screw_rad=screw_rad,
                    magnet_rad=magnet_rad,
                    magnet_depth=magnet_depth,
                    counter_sink=counter_sink)

    if args.vscode:
        from ocp_vscode import show, set_port
        set_port(args.vscode)
        show(base)
    else:
        export_step(base, args.output)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
    
