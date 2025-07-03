# Make a gridfinity base edge for filling out space in a drawer.
#
# Copyright (C) Paul Bone
#
# CC BY 4.0

from argparse import ArgumentParser
from build123d import *

from Edge import Edge

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
        "--loop",
        help="Run in loop mode, generate many base files for different "
        "configurations",
        action="store_true") 
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
    parser.add_argument(
        "--short",
        help="Make the short variant, doesn't support screw holes",
        action="store_true")
    args = parser.parse_args(argv)
        
    if args.loop:
        def make_variant(file_base, obj):
            file = file_base + ".step"
            print(f"Writing {file}")
            export_step(obj, file)
            file = file_base + ".stl"
            print(f"Writing {file}")
            export_stl(obj, file)
            
        for x in range(10, 42, 2):
            for y in range(1, 6):
                make_variant(f"edge-{x}x{y}",
                             Edge(y, x))
                make_variant(f"edge-{x}x{y}-short",
                             Edge(y, x, short=True))

    else:
        edge = Edge(args.x, args.y, short=args.short)
                    
        if args.vscode:
            from ocp_vscode import (show_object,
                                    set_port)
            set_port(args.vscode)
            show_object(edge)
        else:
            if args.output.endswith(".step"):
                export_step(edge, args.output)
            elif args.output.endswith('.stl'):
                export_stl(edge, args.output)
            else:
                print("Unknown output format.")
                exit(1)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

