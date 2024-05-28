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

    args = parser.parse_args(argv)

    x = int(args.x)
    y = int(args.y)
    base = BaseGrid(x, y)

    if args.vscode:
        from ocp_vscode import show, set_port
        set_port(3939)
        show(base)
    else:
        export_step(base, args.output)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
    
