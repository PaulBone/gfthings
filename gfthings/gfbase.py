# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from argparse import ArgumentParser
from build123d import *

from parameters import *
from Base import *

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
        "--loop",
        help="Run in loop mode, generate many base files for different "
        "configurations",
        action="store_true") 
    parser.add_argument(
        "-x",
        help="Number of squares across (default: %(default)s",
        default=4,
        type=int)
    parser.add_argument(
        "-y",
        help="Number of squares deep (default: %(default)s",
        default=4,
        type=int)
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
    
    parser.add_argument(
        "--screw-hole-count",
        help="The number of screw holes in each grid square, 0, 2 or 4" +
        "(default %(default)s",
        default=2,
        type=int)
    parser.add_argument(
        "--screw-hole-pattern-drawer",
        help="Place four screw holes (in addition to --screw-hole-count) " +
        "in a minimal pattern for installation into drawers. ",
        action="store_true")
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

        for x in range(1, 6):
            for y in range(1, 6):
                for screw_count in [0, 2, 4]:
                    make_variant(f"base-{x}x{y}-s{screw_count}",
                                 BaseGrid(x, y, screw_hole_count=screw_count))
                    if screw_count == 0:
                        make_variant(f"base-{x}x{y}-short",
                                     BaseGrid(x, y, screw_hole_count=0, short=True))
                if (x > 3) and (y > 3):
                    make_variant(f"base-{x}x{y}-sd",
                                BaseGrid(x, y, screw_hole_pattern_drawer=True))

    else:
        x = args.x
        y = args.y
        screw_rad = args.screw_diameter/2
        magnet_rad = args.magnet_diameter/2
        magnet_depth = args.magnet_depth
        counter_sink = False
        screw_hole_count = 2 if not args.short else 0
        base = BaseGrid(x, y,
                        screw_rad=screw_rad,
                        magnet_rad=magnet_rad,
                        magnet_depth=magnet_depth,
                        counter_sink=counter_sink,
                        screw_hole_count=screw_hole_count,
                        screw_hole_pattern_drawer=args.screw_hole_pattern_drawer,
                        short=args.short)

        if args.vscode:
            from ocp_vscode import show, set_port
            set_port(args.vscode)
            show(base)
        else:
            if args.output.endswith(".step"):
                export_step(base, args.output)
            elif args.output.endswith('.stl'):
                export_stl(base, args.output)
            else:
                print("Unknown output format.")
                exit(1)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
    
