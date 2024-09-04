# Make a gridfinity base edge for filling out space in a drawer.
#
# Copyright (C) Paul Bone
#
# CC BY 4.0

from argparse import ArgumentParser
from build123d import *

from gfthings.Edge import Edge

def main(argv: list[str] | None = None):
    parser = ArgumentParser(
        description=
            "Generate a edge for a GF base to fill out space in a drawer")
    parser.add_argument(
        "--vscode",
        help="Run in vscode_ocp mode and connect to the given port. " +
             "Do not produce a .step file.",
        default=0,
        type=int)
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename, defaults to `%(default)s'",
        default="edge.step")
    parser.add_argument(
        "-x",
        help="Gridfinity units across, defaults to '%(default)s'",
        default=4,
        type=int)
    parser.add_argument(
        "-y",
        help="Depth of edge spacer in millimeters, defaults to '%(default)s'",
        default=16,
        type=float)

    args = parser.parse_args(argv)

    edge = Edge(args.x, args.y)

    if args.vscode:
        from ocp_vscode import (show_object,
                                set_port)
        set_port(args.vscode)
        show_object(edge)
    else:
        export_step(edge, args.output)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

