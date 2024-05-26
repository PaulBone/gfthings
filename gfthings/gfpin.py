# Make a pin for holding a base plate to plywood.
#
# Copyright (C) Paul Bone
#
# CC BY 4.0

from argparse import ArgumentParser
from build123d import *

from gfthings.Pin import Pin

def main(argv: list[str] | None = None):
    parser = ArgumentParser(
        description="Generate a pin for attaching things to plywood")
    parser.add_argument(
        "--vscode",
        help="Run in vscode_ocp mode and connect to the given port. " +
             "Do not produce a .step file.",
        default=0)
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename, defaults to `%(default)s",
        default="pin.step")

    args = parser.parse_args(argv)

    pin = Pin()

    if args.vscode:
        from ocp_vscode import (show_object,
                                set_port)
        set_port(args.vscode)
        show_object(pin)
    else:
        export_step(pin, args.output)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
