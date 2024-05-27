# Copyright (C) Paul Bone
# CC BY-NC-SA 4.0

from build123d import *

from gfthings.Bin import Bin

def main():
    from ocp_vscode import (show,
                            show_object,
                            reset_show,
                            set_port,
                            set_defaults,
                            get_defaults)
    set_port(3939)

    box = Bin(1, 1, 4, 12.5, divisions=2)
    export_step(box, "bin.step")
    # show_object(box, "test", measure_tools=True)

