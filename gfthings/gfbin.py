# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from argparse import ArgumentParser
from build123d import *

from Bin import (Bin, FunkyBin)

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
        "--loop",
        help="Generate a number of bins in a loop, bins will be named " +
             "bin_\*.step.",
        default=False,
        action="store_true")
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
        "--no-lip",
        help="Don't add the stacking lip",
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
    parser.add_argument(
        "--half-grid",
        help="The base of the bin will fit on a 'half grid' " +
             "that is, 21mm per X/Y gridfinity unit will be " +
             "used for the base, the normal 42mm will be used " +
             "for everything else.  Magnet holes may be broken.",
        action="store_true")
    parser.add_argument(
        "--wall-thickness",
        help="Thickness of bin walls, " +
             "you might adjust this if printing with " +
             "a different nozzle size. " +
             "(The default of %(default)s, " +
             "should work nicely for 0.4mm and 0.6mm nozzles)",
        type=float,
        default=1.2)
    parser.add_argument(
        "--funky",
        help="Generate a 'funky' bin.  This allows the user to make " +
            "non-rectangular bins such as L shapes.  The argument is a " +
            "python expression that evaluates to a 2D rectangular array " +
            "of bools, True for a filled square and False for an empty one. " +
            "In this mode, the x and y parameters are ignored, shelves, " + 
            "scoops and divisions aren't supported.",
        type=str,
        default="")
    
    args = parser.parse_args(argv)
    x = float(args.x)
    y = float(args.y)
    z = int(args.z)
    scoop = float(args.scoop)
    divisions = int(args.divisions)

    bin = None
    funky = args.funky
    if funky != "":
        if funky == "donut":
            funky_expr = [[True, True, True], 
                          [True, False, True],
                          [True, True, True]]
        elif funky == "cross":
            funky_expr = [[False, True, False],
                          [True, True, True],
                          [False, True, False]]
        elif funky == "tetris_l":
            funky_expr = [[True, False],
                          [True, False],
                          [True, True]]
        elif funky == "tetris_j":
            funky_expr = [[False, True],
                          [False, True],
                          [True, True]]
        elif funky == "tetris_t":
            funky_expr = [[False, True, False],
                          [True, True, True]]
        elif funky == "tetris_s":
            funky_expr = [[False, True, True],
                          [True, True, False]]
        elif funky == "tetris_z":
            funky_expr =[[True, True, False],
                         [False, True, True]]
        else:
            funky_expr = eval(args.funky)
        bin = FunkyBin(list(reversed(funky_expr)), z,
                       refined=not args.unrefined,
                       magnet_dia=args.magnet_dia,
                       magnet_depth=args.magnet_height,
                       half_grid=args.half_grid,
                       wall_thickness=args.wall_thickness)
    else:
        bin = Bin(x, y, z, scoop,
              divisions=divisions,
              label=not args.no_label,
              lip=not args.no_lip,
              refined=not args.unrefined,
              magnet_dia=args.magnet_dia,
              magnet_depth=args.magnet_height,
              half_grid=args.half_grid,
              wall_thickness=args.wall_thickness)
    
    if args.loop:
        from pathlib import Path
        for z in (3, 4, 5, 6):
            for x in range(1, 6):
                for y in range(1, 6):
                    for d in range(1, int(x*5/2)) \
                            if (x < 3) and y < 3 else (1,):
                        for s in (0, 10) if y <= 2 else (0,):
                            for l in (True, False):
                                file = "bin_%dx%dx%d_d%d_s%s%s" % \
                                    (x, y, z, d, s, "_label" if l else "")
                                file_stl = Path(file + ".stl")
                                file_step = Path(file + ".step")
                                if file_stl.exists() and file_step.exists():
                                    print("Skipping %s" % file)
                                    continue

                                print("Generating %s" % file)
                                bin = Bin(x, y, z,
                                          divisions=d,
                                          scoop_rad=s,
                                          label=l)
           
                                if not file_stl.exists():
                                    export_stl(bin, str(file_stl))
                                if not file_step.exists():
                                    export_step(bin, str(file_step))

    if args.vscode:
        from ocp_vscode import (show_object,
                                set_port)
        set_port(args.vscode)
        show_object(bin, "bin")
    else:
        if args.output.endswith(".step"):
            export_step(bin, args.output)
        elif args.output.endswith('.stl'):
            export_stl(bin, args.output)
        else:
            print("Unknown output format.")
            exit(1)
        
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
