from ptrace_creator import create_ptrace
import os


class Layout:
    def __init__(self, name, bit, size_x, size_y, is_arbiter):
        self.name = name
        self.bit = bit
        self.size_x = size_x
        self.size_y = size_y
        self.is_arbiter = is_arbiter


path_hotspot = "../../hotspot/"  # path to hotspot executable
path_conf = "../h_conf/"
path_flp = "../h_flp/"
path_ptrace = "../h_ptrace/"
path_output = "../res/"

temp_min = 250  # Kelvin
temp_max = 400  # Kelvin
temp_step = 1  # Kelvin

mux_power_min = 10  # micro W
mux_power_max = 1000  # micro W (included)
mux_power_step = 10  # micro W

layouts = [  # <name>, number of input bits, chip size in dim x [m], chip size in dim y [m],
    # »True« if it is an arbiter puf, »False« if not
    Layout("a_032", 32, 0.1, 0.01, True),
    Layout("a_064", 64, 0.15, 0.01, True),
    Layout("c_002", 1, 0.01, 0.01, False)  # be aware of the halfed bit number -> ptrace_creator is inflexible
]

# compose command line command for hotspot
for layout in layouts:
    for temp in range(temp_min, temp_max, temp_step):
        for mux_power in range(mux_power_min, mux_power_max + mux_power_step, mux_power_step):
            ptrace_file = path_ptrace
            ptrace_file += layout.name + "_" + str(mux_power) + ".ptrace"
            create_ptrace(ptrace_file, layout.bit, mux_power, layout.is_arbiter)
            command = path_hotspot
            command += "hotspot -c "
            command += path_conf
            command += "hotspot.config -f "
            command += path_flp
            command += layout.name
            command += ".flp -p "
            command += ptrace_file
            command += " -ambient "
            command += str(temp)
            command += " -init_temp "
            command += str(temp)
            # optional ToDo: include chip size in hotspot command
            command += " >> "
            command += path_output
            command += layout.name
            command += "_"
            command += str(temp)
            command += "_"
            command += str(mux_power).zfill(4)
            command += ".txt"
            print(command)
            os.system(command)
